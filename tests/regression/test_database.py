"""bots-updatedb: an empty database, the database of bots 3.2.0, the database shipped with bots 4.

`data/botsdb_3.2.0_sqlite` is the database as installed by bots 3.2.0 (bots/install/botsdb of that release).
"""
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIDE = os.path.join(HERE, '_side.py')
BOTS3_DATABASE = os.path.join(HERE, 'data', 'botsdb_3.2.0_sqlite')
PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'UNZ+0+1'"


def sha(path):
    """hash of the content of the database (schema and data; not the file: sqlite may touch the file header)"""
    con = sqlite3.connect(path)
    try:
        return hashlib.sha256('\n'.join(con.iterdump()).encode('utf8')).hexdigest()
    finally:
        con.close()


def schema(path):
    """{table: set of column names} for the tables of bots and django"""
    con = sqlite3.connect(path)
    try:
        tables = [row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
                  if not row[0].startswith('sqlite_')]
        return dict((table, set(row[1] for row in con.execute('PRAGMA table_info("%s")' % table))) for table in tables)
    finally:
        con.close()


def select(path, sql):
    con = sqlite3.connect(path)
    try:
        return con.execute(sql).fetchall()
    finally:
        con.close()


def passthrough(botsrun, name):
    """one file through a route without translation; returns the delivered files"""
    src, out = botsrun.path('src_' + name), botsrun.path('out_' + name)
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(PAYLOAD)
    botsrun.configure(
        channels=[dict(idchannel=name + '_in', inorout='in', type='file', path=src, filename='*.edi'),
                  dict(idchannel=name + '_out', inorout='out', type='file', path=out, filename='*.edi')],
        routes=[dict(idroute=name, seq=1, active=True, fromchannel=name + '_in', tochannel=name + '_out', translateind=2)])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    return os.listdir(out)


def fresh_schema(botsrun):
    """schema of a database made from nothing, in a second file of the same environment"""
    database = botsrun.database
    kept = database + '.kept'
    shutil.move(database, kept)
    code, text = botsrun.updatedb()
    assert code == 0, text
    found = schema(database)
    os.remove(database)
    shutil.move(kept, database)
    return found


def test_upgrade_of_bots3_database(botsrun):
    shutil.copy(BOTS3_DATABASE, botsrun.database)
    before = sha(botsrun.database)

    code, text = botsrun.updatedb('--check')
    assert code == 1 and 'made by bots 3' in text and '--yes-i-have-a-backup' in text, text
    code, text = botsrun.updatedb()
    assert code == 2 and 'Nothing is changed' in text, text
    assert sha(botsrun.database) == before, 'without the confirmation the database is not touched'

    code, text = botsrun.updatedb('--yes-i-have-a-backup')
    assert code == 0 and 'The database is up to date' in text, text
    code, text = botsrun.updatedb('--check')
    assert code == 0 and 'made by bots 4' in text, text

    # the user of bots 3 is still there, with its password
    users = select(botsrun.database, 'SELECT username, is_superuser, password FROM auth_user')
    assert [(name, bool(superuser)) for name, superuser, _password in users] == [('bots', True)]
    assert users[0][2] == select(BOTS3_DATABASE, 'SELECT password FROM auth_user')[0][0]

    # same tables and columns as a new database
    upgraded = schema(botsrun.database)
    new = fresh_schema(botsrun)
    assert set(upgraded) >= set(new), set(new) - set(upgraded)
    missing = dict((table, new[table] - upgraded[table]) for table in new if new[table] - upgraded[table])
    assert not missing, missing
    # ta.statuse is a left-over of bots 2 in the database of bots 3; not used, has a default
    extra = dict((table, upgraded[table] - new[table]) for table in new if upgraded[table] - new[table])
    assert extra == {'ta': {'statuse'}}, extra

    assert passthrough(botsrun, 'up') == ['1.edi']


def test_new_database(botsrun):
    os.remove(botsrun.database)
    code, text = botsrun.updatedb('--check')
    assert code == 1 and 'empty' in text, text
    assert not os.path.exists(botsrun.database) or not schema(botsrun.database), '--check changes nothing'
    code, text = botsrun.updatedb()
    assert code == 0, text
    tables = schema(botsrun.database)
    assert {'ta', 'mutex', 'persist', 'uniek', 'routes', 'channel', 'auth_user'} <= set(tables)
    code, text = botsrun.updatedb('--check')
    assert code == 0 and 'up to date' in text, text
    assert passthrough(botsrun, 'new') == ['1.edi']


def test_shipped_database_is_up_to_date(botsrun):
    """the sqlite database a new environment starts with needs no update"""
    code, text = botsrun.updatedb('--check')
    assert code == 0 and 'up to date' in text, text


def test_database_that_is_not_bots_is_refused(botsrun):
    os.remove(botsrun.database)
    con = sqlite3.connect(botsrun.database)
    con.execute('CREATE TABLE routes (id integer PRIMARY KEY, idroute varchar(35))')
    con.commit()
    con.close()
    before = sha(botsrun.database)
    for args in (['--check'], [], ['--yes-i-have-a-backup']):
        code, text = botsrun.updatedb(*args)
        assert code == 2 and 'not recognised' in text, text
    assert sha(botsrun.database) == before


def test_counters_with_several_processes(botsrun):
    """processes that draw from one (new) counter at the same time never get the same number"""
    # not acceptance-test mode: there the counters are not in the database
    ini = os.path.join(botsrun.envdir, 'config', 'bots.ini')
    with open(ini, encoding='utf8') as f:
        txt = f.read()
    assert 'runacceptancetest = True' in txt
    with open(ini, 'w', encoding='utf8') as f:
        f.write(txt.replace('runacceptancetest = True', 'runacceptancetest = False'))
    results = [os.path.join(botsrun.root, 'draw%s.json' % nr) for nr in range(4)]
    procs = [subprocess.Popen([sys.executable, SIDE, 'draw', 'ut_concurrent', '150', result], env=botsrun.env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE) for result in results]
    errors = [proc.communicate()[1].decode(errors='replace')[-800:] for proc in procs]
    assert [proc.returncode for proc in procs] == [0, 0, 0, 0], errors
    numbers = []
    for result in results:
        with open(result, encoding='utf8') as f:
            drawn = json.load(f)
        assert drawn['by_position'], 'a row can be read as row[0] and as row["name"]'
        assert drawn['numbers'] == sorted(drawn['numbers'])
        numbers += drawn['numbers']
    assert sorted(numbers) == list(range(1, 601))


def test_engine_tells_when_database_has_no_tables(botsrun):
    open(botsrun.database, 'wb').close()          # an empty sqlite database
    assert botsrun.engine() == 3
    with open(os.path.join(botsrun.root, 'engine.log'), encoding='utf8', errors='replace') as f:
        log = f.read()
    assert 'bots-updatedb' in log and 'database is locked' not in log, log[-1500:]

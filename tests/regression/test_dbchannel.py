"""Channel type 'db' with the field 'Database' set: bots makes the connection; the communication script only reads
(incommunicate) or writes (outcommunicate). With SQLite; with BOTS_TEST_DATABASE set (tests/servers.py) the
database of the channels is a new database on that server (MySQL/MariaDB, PostgreSQL, SQL Server)."""
import decimal
import os
import sys
import textwrap

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import servers      # noqa: E402
from bots import dbconnect      # noqa: E402

IN_SCRIPT = '''
def incommunicate(channeldict, dbconnection):
    cursor = dbconnection.cursor()
    cursor.execute("SELECT po, line, item, qty FROM orders WHERE status = %(status)s ORDER BY po, line",
                   {'status': 'Ready'})
    rows = cursor.fetchall()
    cursor.execute("UPDATE orders SET status = %(new)s WHERE status = %(old)s", {'new': 'Send', 'old': 'Ready'})
    orders = {}
    for row in rows:
        orders.setdefault(row['po'], []).append(dict(row))
    return [orders[po] for po in sorted(orders)]
'''
OUT_SCRIPT = '''
def outcommunicate(channeldict, dbconnection, db_object):
    cursor = dbconnection.cursor()
    for line in db_object:
        cursor.execute("INSERT INTO received (po, line, item, qty) VALUES (%(po)s, %(line)s, %(item)s, %(qty)s)", line)
'''
FAILING_OUT_SCRIPT = OUT_SCRIPT + '''
        raise ValueError('stop after the first line')
'''
ORDERS = [('PO2', 1, 'b', '5', 'Ready'), ('PO1', 1, 'a', '2', 'Ready'), ('PO1', 2, 'cé', '3.5', 'Ready'),
          ('PO3', 1, 'x', '1', 'Done')]


def script(botsrun, name, text):
    directory = os.path.join(botsrun.envdir, 'usersys', 'communicationscripts')
    os.makedirs(directory, exist_ok=True)
    open(os.path.join(directory, '__init__.py'), 'a').close()
    with open(os.path.join(directory, name + '.py'), 'w', encoding='utf8') as f:
        f.write(textwrap.dedent(text))


def channel_database(botsrun):
    """fields of the db channels: SQLite, or (BOTS_TEST_DATABASE) a new database on the server; tables made"""
    srv = servers.channel_server()
    if srv is None:
        fields = {'dbengine': 'sqlite', 'path': os.path.join(botsrun.path('db'), 'edi.db')}
    else:
        fields, _name = servers.channel_database(srv)
    text = 'nvarchar' if fields['dbengine'] == 'mssql' else 'varchar'
    with dbconnect.connect_channel(fields) as db:
        cursor = db.cursor()
        cursor.execute('CREATE TABLE orders (po %s(20), line INTEGER, item %s(20), qty DECIMAL(10,2), status %s(10))'
                       % (text, text, text))
        cursor.execute('CREATE TABLE received (po %s(20), line INTEGER, item %s(20), qty DECIMAL(10,2))' % (text, text))
        cursor.executemany('INSERT INTO orders (po, line, item, qty, status) VALUES (%s, %s, %s, %s, %s)',
                           [(po, line, item, decimal.Decimal(qty), status) for po, line, item, qty, status in ORDERS])
    return fields


def select(fields, sql):
    """rows as tuples; decimals as float"""
    with dbconnect.connect_channel(fields) as db:
        cursor = db.cursor()
        cursor.execute(sql)
        return [tuple(float(v) if isinstance(v, decimal.Decimal) else v for v in row.values())
                for row in cursor.fetchall()]


def configure(botsrun, fields, out_script=OUT_SCRIPT):
    script(botsrun, 'db_in', IN_SCRIPT)
    script(botsrun, 'db_out', out_script)
    common = dict(type='db', **fields)
    botsrun.configure(
        channels=[dict(idchannel='db_in', inorout='in', **common), dict(idchannel='db_out', inorout='out', **common)],
        routes=[dict(idroute='dbroute', seq=1, active=True, fromchannel='db_in', tochannel='db_out', translateind=2)])


def test_bots_connects_reads_and_writes(botsrun):
    fields = channel_database(botsrun)
    configure(botsrun, fields)
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    # read: committed by bots (the script does not commit)
    assert select(fields, 'SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY status') == \
        [('Done', 1), ('Send', 3)]
    # written: one message per order
    assert select(fields, 'SELECT po, line, item, qty FROM received ORDER BY po, line') == \
        [('PO1', 1, 'a', 2), ('PO1', 2, 'cé', 3.5), ('PO2', 1, 'b', 5)]
    assert result['report']['send'] == 2


def test_an_error_in_the_script_rolls_back_and_is_reported(botsrun):
    fields = channel_database(botsrun)
    configure(botsrun, fields, FAILING_OUT_SCRIPT)
    botsrun.engine()
    result = botsrun.result()
    assert any('stop after the first line' in text for text in result['errors']), result['errors']
    assert select(fields, 'SELECT COUNT(*) AS n FROM received') == [(0,)]                     # rolled back
    assert select(fields, "SELECT COUNT(*) AS n FROM orders WHERE status='Send'") == [(3,)]   # read is done


@pytest.mark.skipif(servers.channel_server() is not None, reason='the script of this test connects to SQLite itself')
def test_script_with_its_own_connect_is_used_as_in_bots3(botsrun):
    """when the script has connect/disconnect, these are used, also when the field is set"""
    database = channel_database(botsrun)['path']
    own = textwrap.dedent('''
        import sqlite3
        def connect(channeldict):
            connection = sqlite3.connect(channeldict['filename'])
            connection.row_factory = sqlite3.Row
            return connection
        def incommunicate(channeldict, dbconnection):
            rows = [dict(row) for row in dbconnection.execute("SELECT po, line FROM orders WHERE status='Ready'")]
            dbconnection.execute("UPDATE orders SET status='Own' WHERE status='Ready'")
            dbconnection.commit()
            return [rows]
        def disconnect(channeldict, dbconnection):
            dbconnection.close()
        ''')
    script(botsrun, 'db_in', own)
    script(botsrun, 'db_out', OUT_SCRIPT.replace('(po, line, item, qty) VALUES (%(po)s, %(line)s, %(item)s, %(qty)s)',
                                                 '(po, line) VALUES (%(po)s, %(line)s)'))
    botsrun.configure(
        channels=[dict(idchannel='db_in', inorout='in', type='db', dbengine='mysql', path='', filename=database),
                  dict(idchannel='db_out', inorout='out', type='db', dbengine='sqlite', path=database)],
        routes=[dict(idroute='dbroute', seq=1, active=True, fromchannel='db_in', tochannel='db_out', translateind=2)])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    assert select({'dbengine': 'sqlite', 'path': database}, "SELECT COUNT(*) AS n FROM orders WHERE status='Own'") \
        == [(3,)]
    assert select({'dbengine': 'sqlite', 'path': database}, 'SELECT COUNT(*) AS n FROM received') == [(3,)]

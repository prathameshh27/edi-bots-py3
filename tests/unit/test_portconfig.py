"""bots-portconfig: bots.ini and settings.py of bots 3 -> configuration of an environment of this bots."""
import os
import shutil

import pytest

BOTS3_INI = '''
[settings]
maxdays = 60
max_number_errors = 25
get_checklevel = 2
debug = False
[directories]
botssys = botssys7
usersys = usersys7
[webserver]
port = 8087
environment_text = PRODUCTION 7
use_email_address_validation = False
[jobqueue]
enabled = True
lauchfrequency = 3
port = 28097
[dirmonitor1]
path = /home/hje/Bots/botsdev/bots/botssys/infile/stress06/xml
filemask = *.xml
[dirmonitor5]
path = /data/in/orders
filemask = *.edi
route = orders_in
[charsets]
unoz = cp1252
[settings]
maxdays = 90
unknown_thing = 1
[directories]
usersys = usersys7b
'''
BOTS3_SETTINGS = '''# -*- coding: utf-8 -*-
import os
import bots
PROJECT_PATH = os.path.abspath(os.path.dirname(bots.__file__))
MANAGERS = (    #bots will send error reports to the MANAGERS
    ('edi', 'edi@example.com'),
    )
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'reports'
EMAIL_HOST_PASSWORD = 'not-shown'
SERVER_EMAIL = 'bots7@example.com'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'botssys7/sqlitedb/botsdb'),
        }
    }
TIME_ZONE = 'America/Chicago'
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_NAME = 'env7'
SECRET_KEY = 'the-key-of-environment-7'
'''


@pytest.fixture
def configs(botsenv, tmp_path):
    old, new = tmp_path / 'config7', tmp_path / 'config'
    old.mkdir()
    (old / 'bots.ini').write_text(BOTS3_INI, encoding='latin-1')
    (old / 'settings.py').write_text(BOTS3_SETTINGS, encoding='latin-1')
    shutil.copytree(os.path.join(botsenv, 'config'), str(new))
    return str(old), str(new)


def test_report_only_changes_nothing(configs):
    from bots import portconfig
    old, new = configs
    before = dict((name, open(os.path.join(new, name), 'rb').read()) for name in ('bots.ini', 'settings.py'))
    lines = []
    assert portconfig.port(old, new, write=False, out=lines.append)
    assert before == dict((name, open(os.path.join(new, name), 'rb').read()) for name in ('bots.ini', 'settings.py'))
    text = '\n'.join(lines)
    assert '[settings] maxdays = 90' in text and 'Nothing is changed' in text
    assert 'not-shown' not in text and 'the-key-of-environment-7' not in text       # secrets are not printed


def test_bots_ini_is_carried_over(configs):
    from bots import portconfig
    from bots.botsinit import BotsConfig
    old, new = configs
    with open(os.path.join(new, 'bots.ini'), encoding='utf8') as f:
        before = f.read()
    lines = []
    assert portconfig.port(old, new, write=True, out=lines.append)
    with open(os.path.join(new, 'bots.ini'), encoding='utf8') as f:
        after = f.read()
    ini = BotsConfig()
    ini.read_string(after)
    # a value of bots 3 (the last, when it is there twice)
    assert ini.get('settings', 'maxdays') == '90' and ini.get('settings', 'max_number_errors') == '25'
    assert ini.get('settings', 'get_checklevel') == '2'
    assert ini.get('webserver', 'port') == '8087' and ini.get('webserver', 'environment_text') == 'PRODUCTION 7'
    assert ini.get('jobqueue', 'enabled') == 'True' and ini.get('jobqueue', 'port') == '28097'
    # other name in this bots
    assert ini.get('webserver', 'validate_email_address') == 'False'
    assert not ini.has_option('webserver', 'use_email_address_validation')
    # own directory monitor and charset; not the sample monitor of the distribution
    assert ini.get('dirmonitor5', 'path') == '/data/in/orders' and ini.get('dirmonitor5', 'route') == 'orders_in'
    assert ini.get('charsets', 'unoz') == 'cp1252'
    assert '/stress06/xml\n' not in after.replace(before, '') or 'hje' in before
    # not carried: directories, what this bots does not know or use
    old_dirs = BotsConfig()
    old_dirs.read_string(before)
    assert ini.get('directories', 'usersys') == old_dirs.get('directories', 'usersys')
    assert not ini.has_option('settings', 'unknown_thing') and not ini.has_option('jobqueue', 'lauchfrequency')
    text = '\n'.join(lines)
    assert 'unknown_thing: not known to this bots' in text and 'lauchfrequency: not used any more' in text
    # the comments of the new bots.ini are kept, each option is there once
    assert after.count('\n#') >= before.count('\n#')
    assert len([line for line in after.splitlines() if line.startswith('maxdays ')]) == 1
    # a second time: nothing left to do
    again = []
    portconfig.port(old, new, write=True, out=again.append)
    assert again[0] == 'bots.ini: 0 setting(s) changed'


def test_settings_are_carried_over_and_the_environment_starts(configs):
    import subprocess
    import sys
    from bots import portconfig
    old, new = configs
    lines = []
    assert portconfig.port(old, new, write=True, out=lines.append)
    portconfig.port(old, new, write=True, out=lines.append)             # twice: one block
    with open(os.path.join(new, 'settings.py'), encoding='utf8') as f:
        text = f.read()
    assert text.count(portconfig.MARK_START) == 1
    code = ("import sys; from bots import botsinit; botsinit.generalinit(sys.argv[1]); "
            "from django.conf import settings as s; o = s.MAILERS['default']['OPTIONS']; "
            "print('|'.join(str(x) for x in (s.MANAGERS, o['host'], o['port'], o['use_tls'], o['username'], "
            "o['password'], s.SERVER_EMAIL, s.TIME_ZONE, s.SECRET_KEY, s.DATABASES['default']['ENGINE'])))")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for key in ('BOTS_CONFIG_DIR', 'BOTSENV', 'DJANGO_SETTINGS_MODULE'):
        env.pop(key, None)
    proc = subprocess.run([sys.executable, '-c', code, new], capture_output=True, text=True, env=env)
    assert proc.returncode == 0, proc.stderr[-800:]
    assert proc.stdout.strip() == ("(('edi', 'edi@example.com'),)|smtp.example.com|587|True|reports|not-shown|"
                                   "bots7@example.com|America/Chicago|the-key-of-environment-7|"
                                   "django.db.backends.sqlite3")


def test_other_database_is_reported_not_carried(configs):
    from bots import portconfig
    old, new = configs
    with open(os.path.join(old, 'settings.py'), 'w', encoding='latin-1') as f:
        f.write(BOTS3_SETTINGS.replace('django.db.backends.sqlite3', 'django.db.backends.mysql'))
    lines = []
    portconfig.port(old, new, write=False, out=lines.append)
    assert any('DATABASES' in line and 'django.db.backends.mysql' in line and 'by hand' in line for line in lines)


def test_portenv_makes_an_environment_from_bots3(configs, tmp_path):
    """bots-portenv: usersys converted, database copied and upgraded, configuration carried over, usersys checked"""
    import sqlite3
    from bots import portenv
    old_config, _new = configs
    bots3 = tmp_path / 'bots3'
    mappings = bots3 / 'usersys7' / 'mappings' / 'edifact'
    mappings.mkdir(parents=True)
    for directory in (bots3 / 'usersys7', bots3 / 'usersys7' / 'mappings', mappings):
        (directory / '__init__.py').write_text('')
    (mappings / 'old_style.py').write_text("def main(inn,out):\n    print 'python 2 only'\n    half = len(inn.root.children)/2\n")
    shutil.copytree(old_config, str(bots3 / 'config7'))
    (bots3 / 'botssys7' / 'sqlitedb').mkdir(parents=True)
    source_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regression', 'data',
                             'botsdb_3.2.0_sqlite')
    shutil.copyfile(source_db, str(bots3 / 'botssys7' / 'sqlitedb' / 'botsdb'))
    before = dict((str(p), p.read_bytes()) for p in bots3.rglob('*') if p.is_file())
    target = str(tmp_path / 'new7')
    lines = []
    code = portenv.port_environment(str(bots3 / 'usersys7'), str(bots3 / 'config7'),
                                    str(bots3 / 'botssys7' / 'sqlitedb' / 'botsdb'), target, out=lines.append)
    text = '\n'.join(str(line) for line in lines)
    assert code == 1, text                      # done; 1: there is a line to look at (the division)
    # bots 3 is not changed
    assert before == dict((str(p), p.read_bytes()) for p in bots3.rglob('*') if p.is_file())
    with open(os.path.join(target, 'usersys', 'mappings', 'edifact', 'old_style.py'), encoding='utf8') as f:
        assert "print('python 2 only')" in f.read()
    with open(os.path.join(target, 'port-review.txt'), encoding='utf8') as f:
        assert 'division' in f.read()
    assert os.path.isfile(os.path.join(target, 'port-check.json'))
    db = sqlite3.connect(os.path.join(target, 'botssys', 'sqlitedb', 'botsdb'))
    assert db.execute("SELECT COUNT(*) FROM django_migrations WHERE app='bots'").fetchone()[0] >= 6
    db.close()
    with open(os.path.join(target, 'config', 'bots.ini'), encoding='utf8') as f:
        assert 'max_number_errors = 25' in f.read()
    assert '0 do not compile' in text and 'The database is up to date' in text
    # an environment that is there is not overwritten
    assert portenv.port_environment(str(bots3 / 'usersys7'), str(bots3 / 'config7'), None, target, out=lines.append) == 2


def test_relative_channel_paths_become_full_paths_of_the_old_server(tmp_path):
    """--bots3-dir-on-server: a relative path of a file channel (relative to the bots 3 program) gets the full path"""
    import sqlite3
    from bots import portenv
    database = str(tmp_path / 'botsdb')
    db = sqlite3.connect(database)
    db.execute("CREATE TABLE channel (idchannel TEXT, type TEXT, path TEXT, testpath TEXT, archivepath TEXT)")
    db.executemany("INSERT INTO channel VALUES (?,?,?,?,?)", [
        ('rel', 'file', 'botssys7/infile/a', '', ''),
        ('abs', 'file', '/home/edi/in', 'botssys7/test', 'botssys7/archive'),
        ('win', 'mimefile', 'C:/edi/out', '', None),
        ('ftp', 'ftp', 'remote/dir', '', '')])
    db.commit()
    db.close()
    changed = portenv.absolute_channel_paths(database, '/opt/bots/bots')
    assert changed == [('abs', 'testpath', 'botssys7/test', '/opt/bots/bots/botssys7/test'),
                       ('abs', 'archivepath', 'botssys7/archive', '/opt/bots/bots/botssys7/archive'),
                       ('rel', 'path', 'botssys7/infile/a', '/opt/bots/bots/botssys7/infile/a')]
    rows = dict((row[0], row[1:]) for row in sqlite3.connect(database).execute('SELECT * FROM channel'))
    assert rows['rel'][1] == '/opt/bots/bots/botssys7/infile/a' and rows['abs'][1] == '/home/edi/in'
    assert rows['win'][1] == 'C:/edi/out' and rows['ftp'][1] == 'remote/dir'      # full path / not a file channel



def test_local_folders_keep_every_channel_on_this_machine(tmp_path):
    """--local-folders: folders of file channels inside the environment, a testpath for every other channel"""
    import sqlite3
    from bots import portenv
    envdir = str(tmp_path / 'env')
    database = str(tmp_path / 'botsdb')
    db = sqlite3.connect(database)
    db.execute("CREATE TABLE channel (idchannel TEXT, inorout TEXT, type TEXT, path TEXT, testpath TEXT, archivepath TEXT)")
    db.executemany("INSERT INTO channel VALUES (?,?,?,?,?,?)", [
        ('rel', 'in', 'file', 'botssys7/infile/a', '', ''),
        ('linux', 'out', 'file', '/home/edi/public_html/out', '', '/home/edi/archive'),
        ('win', 'in', 'mimefile', r'C:\edi\mail', None, None),
        ('partner', 'out', 'sftp', 'upload', '', '')])
    db.commit()
    db.close()
    changed = portenv.local_folders(database, envdir)
    rows = dict((row[0], row[1:]) for row in sqlite3.connect(database).execute(
        'SELECT idchannel, path, testpath, archivepath FROM channel'))
    channels = os.path.join(envdir, 'channels')
    assert rows['rel'][0] == os.path.join(channels, 'botssys7', 'infile', 'a')
    assert rows['linux'][0] == os.path.join(channels, 'home', 'edi', 'public_html', 'out')
    assert rows['linux'][2] == os.path.join(channels, 'home', 'edi', 'archive')
    assert rows['win'][0] == os.path.join(channels, 'C', 'edi', 'mail')
    assert rows['partner'] == ('upload', os.path.join(channels, 'test', 'out', 'partner'), '')      # path not changed
    assert all(os.path.isdir(new) for _id, _field, _old, new in changed) and len(changed) == 5

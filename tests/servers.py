"""Tests on a database server instead of SQLite.

Set BOTS_TEST_DATABASE to the server, as  <kind>://<user>:<password>@<host>:<port>[?<option>=<value>&...]
    mysql://root:secret@127.0.0.1:3306                       (MySQL or MariaDB)
    postgresql://postgres:secret@127.0.0.1:5432
    mssql://sa:Secret_123@127.0.0.1:1433?TrustServerCertificate=yes
Then every test environment gets its own new database on that server (name botsstab_t_<random>), in which
bots-updatedb makes the tables; the regression tests run on it. The databases are dropped at the end of the
test session. Only databases with names starting with botsstab_t_ are made or dropped.

BOTS_TEST_CHANNEL_DATABASE (same form): only the database of the channels of type 'db' in the tests is on that
server; bots itself stays on SQLite. For a server that is too old for django but fine for a channel.
"""
import os
import re
import sys
import urllib.parse
import uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
PREFIX = 'botsstab_t_'
DJANGO_ENGINES = {'mysql': 'django.db.backends.mysql', 'postgresql': 'django.db.backends.postgresql',
                  'mssql': 'mssql'}
ADMIN_DATABASE = {'mysql': 'mysql', 'postgresql': 'postgres', 'mssql': 'master'}


def server(variable='BOTS_TEST_DATABASE'):
    """the server of BOTS_TEST_DATABASE as a dict, or None (SQLite)"""
    url = os.environ.get(variable)
    if not url:
        return None
    parts = urllib.parse.urlsplit(url)
    kind = {'mariadb': 'mysql', 'postgres': 'postgresql'}.get(parts.scheme, parts.scheme)
    assert kind in DJANGO_ENGINES, 'BOTS_TEST_DATABASE: unknown kind of database "%s"' % parts.scheme
    return {'kind': kind, 'host': parts.hostname or '127.0.0.1', 'port': parts.port,
            'user': urllib.parse.unquote(parts.username or ''), 'password': urllib.parse.unquote(parts.password or ''),
            'options': dict(urllib.parse.parse_qsl(parts.query))}


def admin_connection(srv, database=None):
    """connection with autocommit (CREATE/DROP DATABASE can not be in a transaction)"""
    from bots import dbconnect
    connection = dbconnect.connect(srv['kind'], database or ADMIN_DATABASE[srv['kind']], host=srv['host'],
                                   port=srv['port'], user=srv['user'], password=srv['password'],
                                   options=dict(srv['options']))
    native = connection.native
    if srv['kind'] == 'mysql':
        native.autocommit(True)
    else:
        native.autocommit = True
    return connection


def create_database(srv):
    name = PREFIX + uuid.uuid4().hex[:12]
    connection = admin_connection(srv)
    cursor = connection.cursor()
    if srv['kind'] == 'mysql':
        cursor.execute('CREATE DATABASE `%s` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci' % name)
    elif srv['kind'] == 'postgresql':
        cursor.execute("CREATE DATABASE %s ENCODING 'UTF8'" % name)
    else:
        cursor.execute('CREATE DATABASE [%s]' % name)
    connection.close()
    with open(registry(), 'a', encoding='utf8') as f:
        f.write(name + '\n')
    return name


def registry():
    """file with the names of the databases made by this test process (one per pytest-xdist worker): at the end
    a worker drops only its own databases, not those another worker still uses"""
    base = os.environ.get('BOTS_TEST_TEMP') or os.path.join(os.path.dirname(os.path.dirname(REPO)), '.temp', 'tests')
    if not os.path.isdir(base):
        import tempfile
        base = tempfile.gettempdir()
    return os.path.join(base, 'testdatabases_%s_%s.txt' % (os.environ.get('PYTEST_XDIST_WORKER', 'main'),
                                                          os.environ.get('BOTS_TEST_SESSION', '')))


def drop_databases(srv, names=None, everything=False):
    """drop the given test databases; default: those this test process made; everything: all test databases"""
    if names is None and not everything:
        try:
            with open(registry(), encoding='utf8') as f:
                names = [line.strip() for line in f if line.strip()]
            os.remove(registry())
        except OSError:
            return
    connection = admin_connection(srv)
    cursor = connection.cursor()
    if names is None:
        if srv['kind'] == 'mysql':
            cursor.execute('SHOW DATABASES')
        elif srv['kind'] == 'postgresql':
            cursor.execute('SELECT datname FROM pg_database')
        else:
            cursor.execute('SELECT name FROM sys.databases')
        names = [row[0] for row in cursor.fetchall()]
    for name in names:
        if not name.startswith(PREFIX) or not re.match(r'^\w+$', name):
            continue
        if srv['kind'] == 'mysql':
            cursor.execute('DROP DATABASE IF EXISTS `%s`' % name)
        elif srv['kind'] == 'postgresql':
            cursor.execute('DROP DATABASE IF EXISTS %s WITH (FORCE)' % name)
        else:
            cursor.execute("IF DB_ID('%s') IS NOT NULL BEGIN ALTER DATABASE [%s] SET SINGLE_USER WITH ROLLBACK "
                           "IMMEDIATE; DROP DATABASE [%s] END" % (name, name, name))
    connection.close()


def settings_block(srv, name):
    """python text for the end of settings.py of a test environment"""
    options = {}
    if srv['kind'] == 'mysql':
        options = {'charset': 'utf8mb4'}
    elif srv['kind'] == 'mssql':
        extra = ';'.join('%s=%s' % item for item in srv['options'].items())
        options = {'extra_params': extra} if extra else {}
        if 'python_driver' in srv['options']:
            options = {'python_driver': srv['options']['python_driver'],
                       'extra_params': ';'.join('%s=%s' % item for item in srv['options'].items()
                                                if item[0] != 'python_driver')}
    database = {'ENGINE': DJANGO_ENGINES[srv['kind']], 'NAME': name, 'HOST': srv['host'],
                'PORT': str(srv['port'] or ''), 'USER': srv['user'], 'PASSWORD': srv['password'], 'OPTIONS': options}
    return '\n# test database on a server (tests/servers.py)\nDATABASES = {"default": %r}\n' % database


def channel_server():
    """server for the database of channels of type db: BOTS_TEST_CHANNEL_DATABASE (only the channels, bots itself
    on SQLite), else BOTS_TEST_DATABASE"""
    return server('BOTS_TEST_CHANNEL_DATABASE') or server()


def channel_database(srv):
    """fields of a channel of type db for a new test database on the server: (fields, name)"""
    name = create_database(srv)
    fields = {'dbengine': srv['kind'], 'host': srv['host'], 'port': srv['port'] or 0, 'username': srv['user'],
              'secret': srv['password'], 'path': name,
              'parameters': ';'.join('%s=%s' % item for item in srv['options'].items())}
    return fields, name

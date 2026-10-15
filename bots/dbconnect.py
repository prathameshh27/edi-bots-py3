# -*- coding: utf-8 -*-
"""
Connections to the databases bots works with: MySQL/MariaDB, PostgreSQL, SQLite and Microsoft SQL Server.

Used for
 - channels of type 'db': bots opens the connection from the fields of the channel, a communication script
   only has to read or write (see communication.db);
 - the database of bots itself, for bots-engine (see botsinit.connect), on SQL Server.

Whatever the database, a connection made here behaves the same:
 - cursor.execute(sql, params) with parameters as %(name)s and a dict, or %s and a list/tuple (as with MySQL and
   PostgreSQL drivers; for SQLite and SQL Server this is translated);
 - a row can be used as row['column'] and as row[0];
 - commit(), rollback(), close(); the connection of the driver itself is 'native'.
Nothing is committed by itself: a script commits.

The driver is a separate library, installed with bots' install options:
    mysql: mysqlclient (module MySQLdb)        postgresql: psycopg (or psycopg2)
    mssql: mssql-python, or pyodbc with an ODBC driver for SQL Server            sqlite: part of python
"""
import decimal
import re
import sqlite3

from .botslib import gettext as _gettext
from .exceptions import BotsError

ENGINES = {
    'mysql': 'MySQL / MariaDB',
    'postgresql': 'PostgreSQL',
    'sqlite': 'SQLite',
    'mssql': 'Microsoft SQL Server',
}
DEFAULT_PORTS = {'mysql': 3306, 'postgresql': 5432, 'mssql': 1433}
# SQLite has no decimal type: store a decimal as its text (exact; a NUMERIC column makes it a number again)
sqlite3.register_adapter(decimal.Decimal, str)
def _(text):
    """translated text; also outside bots (no django settings), eg in a script or a test"""
    try:
        return _gettext(text)
    except Exception:       # pylint: disable=broad-exception-caught
        return text


PYFORMAT = re.compile(r'%\((?P<name>[^)]+)\)s')
POSITIONAL = re.compile(r'%s')


class DbConnectError(BotsError):
    """the database can not be reached, or a driver is not installed"""


def parse_options(text):
    """'key=value' pairs, separated by ';' or new lines (the channel field 'parameters') -> dict.
    Values 'true'/'false' and whole numbers become bool/int."""
    options = {}
    for part in re.split(r'[;\r\n]+', text or ''):
        if '=' not in part:
            continue
        key, value = (item.strip() for item in part.split('=', 1))
        if not key:
            continue
        if value.lower() in ('true', 'yes'):
            value = True
        elif value.lower() in ('false', 'no'):
            value = False
        elif value.isdigit():
            value = int(value)
        options[key] = value
    return options


class Row(dict):
    """a row: a dict (as MySQLdb's DictCursor gives, which communication scripts of bots 3 use), that can also be
    used by position: row[0]."""

    def __init__(self, names, values):
        super().__init__(zip(names, values))
        self._values = tuple(values)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        return super().__getitem__(key)



class Cursor:
    """cursor with the same behaviour for every database (see the module text)"""

    def __init__(self, connection, native):
        self.connection = connection
        self.native = native

    def _translate(self, sql, params):
        engine = self.connection.engine
        if engine in ('mysql', 'postgresql') or params is None:
            return self.connection.adapt_sql(sql), params
        if isinstance(params, dict):
            names = []

            def placeholder(match):
                names.append(match.group('name'))
                return '?'
            sql = PYFORMAT.sub(placeholder, sql)
            params = [params[name] for name in names]
        else:
            sql = POSITIONAL.sub('?', sql)
        return self.connection.adapt_sql(sql.replace('%%', '%')), list(params)

    def execute(self, sql, params=None):
        sql, params = self._translate(sql, params)
        if params is None:
            self.native.execute(sql)
        else:
            self.native.execute(sql, params)
        return self

    def executemany(self, sql, seq_of_params):
        seq = list(seq_of_params)
        if not seq:
            return self
        translated, _first = self._translate(sql, seq[0])
        self.native.executemany(translated, [self._translate(sql, params)[1] for params in seq])
        return self

    def _names(self):
        return [column[0] for column in (self.native.description or [])]

    def _row(self, values):
        if values is None:
            return None
        if isinstance(values, dict):
            return Row(list(values.keys()), list(values.values()))
        return Row(self._names(), list(values))

    def fetchone(self):
        return self._row(self.native.fetchone())

    def fetchall(self):
        return [self._row(values) for values in self.native.fetchall()]

    def fetchmany(self, size=None):
        rows = self.native.fetchmany(size) if size else self.native.fetchmany()
        return [self._row(values) for values in rows]

    def __iter__(self):
        while True:
            row = self.fetchone()
            if row is None:
                return
            yield row

    @property
    def description(self):
        return self.native.description

    @property
    def rowcount(self):
        return self.native.rowcount

    @property
    def lastrowid(self):
        """id of the row that the last INSERT made"""
        if self.connection.engine == 'postgresql':
            self.native.execute('SELECT lastval()')
            return self.native.fetchone()[0]
        if self.connection.engine == 'mssql':
            self.native.execute('SELECT CAST(@@IDENTITY AS bigint)')
            value = self.native.fetchone()[0]
            return int(value) if value is not None else None
        return self.native.lastrowid

    def close(self):
        self.native.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class Connection:
    """connection with the same behaviour for every database (see the module text)"""

    def __init__(self, engine, native, words=()):
        self.engine = engine
        self.native = native
        # words that are reserved in this database and are column names in bots (eg 'merge' in SQL Server)
        self._words = re.compile(r'(?<![\[\w"`])(%s)(?![\]\w"`])' % '|'.join(words), re.I) if words else None

    def adapt_sql(self, sql):
        if self._words is not None:
            sql = self._words.sub(r'[\1]', sql)
        return sql

    def cursor(self):
        return Cursor(self, self.native.cursor())

    def commit(self):
        self.native.commit()

    def rollback(self):
        self.native.rollback()

    def close(self):
        self.native.close()

    def __enter__(self):
        return self

    def __exit__(self, kind, *args):
        if kind is None:
            self.commit()
        else:
            self.rollback()
        self.close()


def _driver(name):
    try:
        return __import__(name, fromlist=['_'])
    except ImportError as exc:
        raise DbConnectError(
            _('To connect to %(database)s python library "%(library)s" is needed: it is not installed.'),
            {'database': name, 'library': name}) from exc


def mssql_odbc_driver(pyodbc):
    """the newest ODBC driver for SQL Server that is installed"""
    found = [name for name in pyodbc.drivers() if 'SQL Server' in name]
    for wanted in ('ODBC Driver 18 for SQL Server', 'ODBC Driver 17 for SQL Server'):
        if wanted in found:
            return wanted
    if found:
        return sorted(found)[-1]
    raise DbConnectError(_('No ODBC driver for SQL Server is installed (eg "ODBC Driver 18 for SQL Server").'))


def connect(engine, database, host=None, port=None, user=None, password=None, options=None, timeout=30):
    """
    Open a connection. engine: 'mysql', 'postgresql', 'sqlite' or 'mssql'; database: its name, for SQLite the
    path of the file. options: extra arguments for the driver (dict, or text as parse_options takes).
    """
    # pylint: disable=too-many-arguments, too-many-branches
    if isinstance(options, str):
        options = parse_options(options)
    options = dict(options or {})
    engine = (engine or '').lower()
    if engine in ('mariadb',):
        engine = 'mysql'
    if engine in ('postgres', 'pg'):
        engine = 'postgresql'
    if engine in ('sqlserver', 'microsoft', 'ms sql', 'mssqlserver'):
        engine = 'mssql'
    port = int(port) if port else DEFAULT_PORTS.get(engine)
    try:
        if engine == 'sqlite':
            native = sqlite3.connect(database, timeout=timeout, **options)
            return Connection(engine, native)
        if engine == 'mysql':
            mysqldb = _driver('MySQLdb')
            options.setdefault('charset', 'utf8mb4')
            native = mysqldb.connect(host=host or 'localhost', port=port, db=database, user=user or '',
                                     passwd=password or '', connect_timeout=timeout, **options)
            return Connection(engine, native)
        if engine == 'postgresql':
            try:
                psycopg = __import__('psycopg')
            except ImportError:
                psycopg = _driver('psycopg2')
            native = psycopg.connect(host=host or 'localhost', port=port, dbname=database, user=user or None,
                                     password=password or None, connect_timeout=timeout, **options)
            return Connection(engine, native)
        if engine == 'mssql':
            return _connect_mssql(database, host, port, user, password, options, timeout)
    except BotsError:
        raise
    except Exception as exc:
        raise DbConnectError(
            _('Could not connect to %(engine)s database "%(database)s" on "%(host)s": %(error)s'),
            {'engine': ENGINES.get(engine, engine), 'database': database, 'host': host or '',
             'error': '%s: %s' % (exc.__class__.__name__, exc)}) from exc
    raise DbConnectError(_('Unknown kind of database "%(engine)s"; known are: %(known)s.'),
                         {'engine': engine, 'known': ', '.join(ENGINES)})


# words that are column names of bots and reserved in SQL Server
MSSQL_RESERVED = ('merge',)


def _connect_mssql(database, host, port, user, password, options, timeout):
    """SQL Server: with mssql-python if installed (no ODBC driver needed), else pyodbc."""
    # pylint: disable=too-many-arguments
    driver = str(options.pop('python_driver', '')).lower()
    server = '%s,%s' % (host or 'localhost', port)
    parts = {'Server': server, 'Database': database}
    if user:
        parts.update(UID=user, PWD=password or '')
    else:
        parts['Trusted_Connection'] = 'yes'
    # TLS: as the drivers do (Encrypt=yes); TrustServerCertificate=yes for a server with its own certificate
    for key, value in options.items():
        parts[key] = 'yes' if value is True else 'no' if value is False else value
    use_pyodbc = driver == 'pyodbc' or 'Driver' in parts
    if not use_pyodbc:
        try:
            mssql_python = __import__('mssql_python')
        except ImportError:
            use_pyodbc = True
    if use_pyodbc:
        pyodbc = _driver('pyodbc')
        parts.setdefault('Driver', '{%s}' % mssql_odbc_driver(pyodbc))
        native = pyodbc.connect(';'.join('%s=%s' % item for item in parts.items()), timeout=timeout, autocommit=False)
    else:
        native = mssql_python.connect(';'.join('%s=%s' % item for item in parts.items()), autocommit=False)
    return Connection('mssql', native, MSSQL_RESERVED)


def connect_channel(channeldict):
    """Connection for a channel of type 'db': kind of database from field 'dbengine'; database from 'path' (for
    SQLite: the file), or else from 'filename'; host, port, username, secret; driver options from 'parameters'."""
    return connect(
        channeldict.get('dbengine'),
        channeldict.get('path') or channeldict.get('filename'),
        host=channeldict.get('host'), port=channeldict.get('port'), user=channeldict.get('username'),
        password=channeldict.get('secret'), options=channeldict.get('parameters'))


def connect_django(settings_dict):
    """Connection to the database of bots itself as django has it in settings.py (for SQL Server)."""
    engine = settings_dict['ENGINE']
    options = dict(settings_dict.get('OPTIONS') or {})
    kind = {'mssql': 'mssql', 'sql_server.pyodbc': 'mssql'}.get(engine)
    if kind != 'mssql':
        raise DbConnectError(_('connect_django is for SQL Server; database engine is "%(engine)s".'), {'engine': engine})
    extra = parse_options(options.pop('extra_params', '') or '')
    if options.get('driver'):
        extra['Driver'] = '{%s}' % options['driver']
    if 'python_driver' in options:
        extra['python_driver'] = options['python_driver']
    return connect('mssql', settings_dict['NAME'], host=settings_dict.get('HOST'), port=settings_dict.get('PORT'),
                   user=settings_dict.get('USER'), password=settings_dict.get('PASSWORD'), options=extra)

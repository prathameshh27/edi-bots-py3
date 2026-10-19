"""
Bots sqlite lib
"""
import re
import sqlite3

from . import botsglobal
from .exceptions import BotsConfigError

reformatparamstyle = re.compile(r"%\((?P<name>[^)]+)\)s")

sqlite3.register_adapter(bool, int)                            # python type -> SQL type
sqlite3.register_converter("BOOLEAN", lambda s: bool(int(s)))  # SQL type -> python type


def connect(database: str) -> sqlite3.Connection:
    """
    :param database:

    :return sqlite3 database connection
    """
    con = sqlite3.connect(
        database,
        factory=BotsConnection,
        detect_types=sqlite3.PARSE_DECLTYPES,
        timeout=99.0,
        isolation_level='EXCLUSIVE'
    )
    con.row_factory = sqlite3.Row
    for pragma in pragmas():
        con.execute(pragma)
    return con


SYNCHRONOUS = ('NORMAL', 'FULL', 'OFF')


def pragmas():
    """
    The statements every SQLite connection of bots starts with (the engine's and django's).
    WAL (write-ahead log): the database is never damaged by a power cut or a crash of the system, and it is faster
    than the rollback journal (the engine about twice as fast). bots.ini [settings] sqlite_synchronous:
    NORMAL (default; a power cut can lose the last commits), FULL (nothing is lost; 3 to 6 times slower),
    OFF (as bots did before 4.0; a power cut can damage the database).
    """
    value = botsglobal.ini.get('settings', 'sqlite_synchronous', 'NORMAL') if botsglobal.ini else 'NORMAL'
    if value.upper() not in SYNCHRONOUS:
        raise BotsConfigError(
            f'bots.ini [settings] sqlite_synchronous = {value}: it can be {", ".join(SYNCHRONOUS)}.')
    return ['PRAGMA journal_mode=WAL', f'PRAGMA synchronous={value.upper()}']


def on_connection_created(sender, connection, **kwargs):  # pylint: disable=unused-argument
    """django's connections (the web server, and the engine with django_db_connection): set as the engine's"""
    if connection.vendor == 'sqlite':
        for pragma in pragmas():
            connection.connection.execute(pragma)


class BotsConnection(sqlite3.Connection):
    """Bots sqlite3.Connection class"""
    # pylint: disable=too-few-public-methods

    def cursor(self) -> sqlite3.Cursor:
        """sqlite3.Connection.cursor"""
        return sqlite3.Connection.cursor(self, factory=BotsCursor)


class BotsCursor(sqlite3.Cursor):
    """
    bots engine uses:
        SELECT * FROM ta WHERE idta=%(idta)s,{'idta':12345})
    SQLite wants:
        SELECT * FROM ta WHERE idta=:idta, {'idta': 12345}
    """
    # pylint: disable=too-few-public-methods

    def execute(self, string, parameters=None):
        """sqlite3.Cursor.execute"""
        if parameters is None:
            sqlite3.Cursor.execute(self, string)
        else:
            query = reformatparamstyle.sub(r":\g<name>", string)
            # botsglobal.logger.debug('sqlite3.Cursor.execute("""%s""")', query)
            sqlite3.Cursor.execute(self, query, parameters)

"""bots.dbconnect: one behaviour for every database (here with SQLite; the servers in tests/database/dbchannels.py)."""
import pytest

from bots import dbconnect


def test_options_of_the_channel_field_parameters():
    assert dbconnect.parse_options('sslmode=require; connect_timeout=5\nTrustServerCertificate=yes;x') == {
        'sslmode': 'require', 'connect_timeout': 5, 'TrustServerCertificate': True}
    assert dbconnect.parse_options('') == {} and dbconnect.parse_options(None) == {}


def test_sqlite_connection_behaves_as_the_others(tmp_path):
    path = str(tmp_path / 'orders.db')
    with dbconnect.connect('sqlite', path) as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE orders (po TEXT, line INTEGER, status TEXT, [merge] INTEGER)')
        cursor.executemany('INSERT INTO orders (po, line, status) VALUES (%(po)s, %(line)s, %(status)s)',
                           [{'po': 'PO1', 'line': 1, 'status': 'Ready'}, {'po': 'PO1', 'line': 2, 'status': 'Ready'},
                            {'po': 'PO2', 'line': 1, 'status': 'Done'}])
        cursor.execute('INSERT INTO orders (po, line, status) VALUES (%s, %s, %s)', ('PO3', 1, '100%'))
        assert cursor.lastrowid == 4
    connection = dbconnect.connect('sqlite', path)
    cursor = connection.cursor()
    cursor.execute("SELECT po, line, status FROM orders WHERE status=%(status)s ORDER BY line", {'status': 'Ready'})
    rows = cursor.fetchall()
    # a row is a dict (as the DictCursor of MySQLdb that scripts of bots 3 use), and can be used by position
    assert rows == [{'po': 'PO1', 'line': 1, 'status': 'Ready'}, {'po': 'PO1', 'line': 2, 'status': 'Ready'}]
    assert rows[1][1] == 2 and rows[1]['line'] == 2 and list(rows[0].items())[0] == ('po', 'PO1')
    cursor.execute("SELECT status FROM orders WHERE status LIKE %s", ['%\\%'])
    cursor.execute("SELECT COUNT(*) AS n FROM orders")
    assert cursor.fetchone()['n'] == 4
    cursor.execute("UPDATE orders SET status='Send' WHERE status='Ready'")
    assert cursor.rowcount == 2
    connection.rollback()
    cursor.execute("SELECT COUNT(*) AS n FROM orders WHERE status='Ready'")
    assert cursor.fetchone()[0] == 2
    connection.close()


def test_channel_fields_and_unknown_database(tmp_path):
    path = str(tmp_path / 'c.db')
    connection = dbconnect.connect_channel({'dbengine': 'sqlite', 'path': path, 'filename': 'not used', 'host': '',
                                            'port': 0, 'username': '', 'secret': '', 'parameters': ''})
    assert connection.engine == 'sqlite'
    connection.close()
    # database name in 'filename' (as the scripts of bots 3 did) when 'path' is empty
    connection = dbconnect.connect_channel({'dbengine': 'sqlite', 'path': '', 'filename': path})
    connection.close()
    with pytest.raises(dbconnect.DbConnectError, match='Unknown kind of database'):
        dbconnect.connect('oracle', 'x')


def test_mssql_reserved_column_name_is_quoted():
    connection = dbconnect.Connection('mssql', native=None, words=dbconnect.MSSQL_RESERVED)
    assert connection.adapt_sql('SELECT idta FROM ta WHERE merge=? AND [merge]=? AND emerge=1') == \
        'SELECT idta FROM ta WHERE [merge]=? AND [merge]=? AND emerge=1'
    cursor = dbconnect.Cursor(connection, native=None)
    assert cursor._translate('UPDATE ta SET merge=%(m)s WHERE idta=%(i)s AND x LIKE %(p)s', {'i': 7, 'm': 1, 'p': 'a%'}) \
        == ('UPDATE ta SET [merge]=? WHERE idta=? AND x LIKE ?', [1, 7, 'a%'])      # pylint: disable=protected-access


def test_missing_driver_is_explained(monkeypatch):
    import builtins
    real_import = builtins.__import__

    def no_mysqldb(name, *args, **kwargs):
        if name == 'MySQLdb':
            raise ImportError(name)
        return real_import(name, *args, **kwargs)
    monkeypatch.setattr(builtins, '__import__', no_mysqldb)
    with pytest.raises(dbconnect.DbConnectError, match='MySQLdb.*not installed'):
        dbconnect.connect('mysql', 'x', host='127.0.0.1')

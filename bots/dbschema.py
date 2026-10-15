"""
Database tables of bots-engine that are not managed by django: ta, mutex, persist, uniek.

The definitions are in bots/sql/ (per database vendor).
Used by the migrations (so 'migrate' gives a complete database) and by bots-updatedb.
"""
import os
import re

ENGINE_TABLES = ('ta', 'mutex', 'persist', 'uniek')
SQLDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql')
VARCHAR = re.compile(r'^\s*(\w+)\s+n?varchar\s*\(\s*(\d+)\s*\)(.*?),?\s*$', re.IGNORECASE)
PRIMARY_KEY = re.compile(r'PRIMARY\s+KEY\s*(\(([^)]*)\))?', re.IGNORECASE)


def sqlfile(table, vendor):
    """file with the definition of table; vendor as in django: 'sqlite', 'postgresql', 'mysql', 'microsoft'."""
    for name in (f'{table}.{vendor}.sql', f'{table}.sql'):
        path = os.path.join(SQLDIR, name)
        if os.path.isfile(path):
            return path
    raise ValueError(f'No definition of table "{table}" for database "{vendor}".')


def statements(table, vendor):
    """the sql-statements that create table (and its indexes)."""
    with open(sqlfile(table, vendor), encoding='utf-8') as sqlf:
        return [statement.strip() for statement in sqlf.read().split(';') if statement.strip()]


def varchar_columns(table, vendor):
    """
    varchar columns as defined for table: {name: (length, rest of definition, is part of primary key)}
    """
    with open(sqlfile(table, vendor), encoding='utf-8') as sqlf:
        lines = sqlf.read().splitlines()
    keys = set()
    for line in lines:
        found = PRIMARY_KEY.search(line)
        if found and line.strip().upper().startswith('PRIMARY'):
            keys.update(name.strip() for name in found.group(2).split(','))
    columns = {}
    for line in lines:
        found = VARCHAR.match(line)
        if found:
            name, length, rest = found.group(1), int(found.group(2)), found.group(3)
            is_key = name in keys or bool(PRIMARY_KEY.search(rest))
            columns[name] = (length, PRIMARY_KEY.sub('', rest).strip(), is_key)
    return columns


def current_lengths(cursor, connection, table):
    """lengths of the character columns of table in the database: {name: length}"""
    schema = {'mysql': 'DATABASE()', 'microsoft': 'SCHEMA_NAME()'}.get(connection.vendor, 'current_schema()')
    cursor.execute(
        'SELECT column_name, character_maximum_length FROM information_schema.columns'
        f' WHERE table_schema = {schema} AND table_name = %s', [table])
    return dict((row[0], row[1]) for row in cursor.fetchall() if row[1])


def narrow_columns(connection, cursor=None):
    """
    columns of the engine tables that are narrower in the database than defined: [(table, column, is, should be)].
    Not for sqlite: sqlite does not enforce the length of a column.
    """
    if connection.vendor == 'sqlite':
        return []
    if cursor is None:
        with connection.cursor() as newcursor:
            return narrow_columns(connection, newcursor)
    existing = set(connection.introspection.table_names(cursor))
    found = []
    for table in ENGINE_TABLES:
        if table not in existing:
            continue
        lengths = current_lengths(cursor, connection, table)
        for name, (length, _rest, _is_key) in varchar_columns(table, connection.vendor).items():
            if name in lengths and lengths[name] < length:
                found.append((table, name, lengths[name], length))
    return found


def ensure_engine_tables(connection):
    """
    Create the engine tables that do not exist; widen the columns that are narrower than defined
    (a database made by bots 3). Nothing is dropped, nothing is made narrower.
    Returns list of texts: what is done.
    """
    done = []
    quote = connection.ops.quote_name
    with connection.cursor() as cursor:
        existing = set(connection.introspection.table_names(cursor))
        for table in ENGINE_TABLES:
            if table not in existing:
                for statement in statements(table, connection.vendor):
                    cursor.execute(statement)
                done.append(f'created table {table}')
        for table, name, current, length in narrow_columns(connection, cursor):
            _length, rest, is_key = varchar_columns(table, connection.vendor)[name]
            if connection.vendor == 'mysql':
                if is_key and 'NOT NULL' not in rest.upper():
                    rest += ' NOT NULL'
                cursor.execute(f'ALTER TABLE {quote(table)} MODIFY {quote(name)} varchar({length}) {rest}')
            elif connection.vendor == 'microsoft':
                rest = 'NOT NULL' if is_key or 'NOT NULL' in rest.upper() else 'NULL'
                cursor.execute(f'ALTER TABLE {quote(table)} ALTER COLUMN {quote(name)} nvarchar({length}) {rest}')
            else:
                cursor.execute(f'ALTER TABLE {quote(table)} ALTER COLUMN {quote(name)} TYPE varchar({length})')
            done.append(f'{table}.{name}: length {current} -> {length}')
    return done

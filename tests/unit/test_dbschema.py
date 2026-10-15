"""Parts of bots-updatedb that do not need a database of bots 3: column definitions, permissions."""
import pytest


@pytest.mark.parametrize('vendor', ['sqlite', 'postgresql', 'mysql'])
def test_definitions_of_engine_tables(vendor):
    from bots import dbschema
    for table in dbschema.ENGINE_TABLES:
        assert dbschema.statements(table, vendor)[0].upper().startswith('CREATE TABLE')
    ta = dbschema.varchar_columns('ta', vendor)
    assert (ta['reference'][0], ta['divtext'][0], ta['botskey'][0], ta['rsrv1'][0], ta['rsrv5'][0]) == (256, 128, 64, 128, 256)
    assert ta['reference'][1:] == ("DEFAULT ''", False)
    # keys: 'PRIMARY KEY' is not part of the definition used to change the column
    assert dbschema.varchar_columns('uniek', vendor) == {'domein': (128, 'NOT NULL', True)}
    persist = dbschema.varchar_columns('persist', vendor)
    assert persist == {'domein': (70, '', True), 'botskey': (64, '', True)}


def test_model_and_definition_have_the_same_lengths(botsenv):
    from bots import dbschema, models
    for model in (models.ta, models.uniek, models.persist):
        defined = dbschema.varchar_columns(model._meta.db_table, 'postgresql')
        for name, (length, _rest, _key) in defined.items():
            assert model._meta.get_field(name).max_length == length, (model._meta.db_table, name)


def test_view_permissions_for_users_of_bots3(botsenv):
    from django.contrib.auth.models import Group, Permission, User
    from bots import botsupdatedb

    def perm(codename):
        return Permission.objects.get(content_type__app_label='bots', codename=codename)

    def codenames(related):
        return set(related.filter(codename__startswith='view_').values_list('codename', flat=True))

    editor = User.objects.create_user('ut_editor', password='x')
    editor.user_permissions.add(perm('change_channel'), perm('change_routes'))
    inactive = User.objects.create_user('ut_inactive', password='x', is_active=False)
    inactive.user_permissions.add(perm('change_partner'))
    group = Group.objects.create(name='ut_group')
    group.permissions.add(perm('change_translate'))

    assert botsupdatedb.grant_view_permissions() >= 7
    everyone = {'view_report', 'view_filereport', 'view_ta'}
    assert codenames(editor.user_permissions) == everyone | {'view_channel', 'view_routes'}
    assert codenames(inactive.user_permissions) == {'view_partner'}
    assert codenames(group.permissions) == {'view_translate'}
    assert botsupdatedb.grant_view_permissions() == 0, 'nothing to give the second time'


def test_row_by_name_and_by_position():
    """rows of the engine's own postgresql connection (psycopg 3)"""
    from bots import botsinit

    class Column:
        def __init__(self, name):
            self.name = name

    class Cursor:
        description = [Column('idta'), Column('filename')]

    row = botsinit.botsrow_factory(Cursor())((7, 'a.edi'))
    assert (row['idta'], row['filename'], row[0], row[1], row[0:2]) == (7, 'a.edi', 7, 'a.edi', (7, 'a.edi'))
    assert dict(row) == {'idta': 7, 'filename': 'a.edi'} and row.get('nothere') is None
    with pytest.raises(KeyError):
        row['nothere']          # pylint: disable=pointless-statement


def test_only_driver_options_go_to_the_driver():
    from bots import botsinit
    options = {'sslmode': 'require', 'isolation_level': 1, 'pool': True, 'server_side_binding': True, 'charset': 'utf8mb4'}
    assert botsinit.driver_options(options) == {'sslmode': 'require', 'charset': 'utf8mb4'}
    assert botsinit.driver_options(None) == {}

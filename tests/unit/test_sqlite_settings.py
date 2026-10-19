"""SQLite in WAL mode for every connection of bots (the engine's and django's), with bots.ini [settings]
sqlite_synchronous: NORMAL (default), FULL or OFF. Before 4.0 bots used synchronous OFF in the rollback journal: a power
cut could damage the database."""
import pytest


def test_every_sqlite_connection_is_in_wal_with_synchronous_normal(botsenv):
    from django.db import connection
    from bots import botsglobal
    connection.ensure_connection()
    for cursor in (connection.cursor(), botsglobal.db.cursor()):
        cursor.execute('PRAGMA journal_mode')
        assert cursor.fetchone()[0] == 'wal'
        cursor.execute('PRAGMA synchronous')
        assert cursor.fetchone()[0] == 1                # NORMAL


@pytest.mark.parametrize('value, synchronous', [('', 'NORMAL'), ('full', 'FULL'), ('OFF', 'OFF')])
def test_the_setting_comes_from_bots_ini(botsenv, monkeypatch, value, synchronous):
    from bots import botsglobal, botssqlite
    monkeypatch.setattr(botsglobal.ini, 'get', lambda section, option, default='': value or default)
    assert botssqlite.pragmas() == ['PRAGMA journal_mode=WAL', f'PRAGMA synchronous={synchronous}']


def test_a_value_that_is_not_allowed_says_which_are(botsenv, monkeypatch):
    from bots import botsglobal, botssqlite
    from bots.exceptions import BotsConfigError
    monkeypatch.setattr(botsglobal.ini, 'get', lambda section, option, default='': 'fast')
    with pytest.raises(BotsConfigError, match='NORMAL, FULL, OFF'):
        botssqlite.pragmas()


def test_a_new_connection_of_the_engine_gets_the_setting(botsenv, monkeypatch, tmp_path):
    from bots import botsglobal, botssqlite
    monkeypatch.setattr(botsglobal.ini, 'get', lambda section, option, default='': 'FULL')
    connection = botssqlite.connect(str(tmp_path / 'one.sqlite'))
    try:
        assert connection.execute('PRAGMA journal_mode').fetchone()[0] == 'wal'
        assert connection.execute('PRAGMA synchronous').fetchone()[0] == 2           # FULL
    finally:
        connection.close()

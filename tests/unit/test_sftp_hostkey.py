"""SFTP: the server's host key is checked against a known_hosts file before a password or key is sent
(bots.ini [settings] sftp_known_hosts, sftp_unknown_host), against a local server (_sftp_server.py)."""
import os
import subprocess
import sys

import pytest

paramiko = pytest.importorskip('paramiko')

HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def server(botsenv, tmp_path):
    """a local sftp server with a fixed host key; yields (port, host key, folder of the test)"""
    host_key = paramiko.RSAKey.generate(2048)
    host_key.write_private_key_file(str(tmp_path / 'host_key'))
    home = tmp_path / 'home'
    home.mkdir()
    process = subprocess.Popen([sys.executable, os.path.join(HERE, '_sftp_server.py'), str(home), 'bots', 'botspw', '',
                                str(tmp_path / 'host_key')], stdout=subprocess.PIPE, text=True)
    try:
        yield int(process.stdout.readline()), host_key, tmp_path
    finally:
        process.kill()
        process.wait(10)


@pytest.fixture
def settings(server):
    """sftp_known_hosts in the folder of the test; the settings are taken away again afterwards"""
    from bots import botsglobal
    known = server[2] / 'known_hosts'
    botsglobal.ini.set('settings', 'sftp_known_hosts', str(known))
    yield known
    for option in ('sftp_known_hosts', 'sftp_unknown_host'):
        botsglobal.ini.remove_option('settings', option)


def connect(port):
    from bots import communication
    channel = {'idchannel': 'ut_sftp', 'type': 'sftp', 'inorout': 'in', 'host': '127.0.0.1', 'port': port,
               'username': 'bots', 'secret': 'botspw', 'keyfile': '', 'parameters': '', 'path': '', 'debug': None}
    session = communication.sftp(channel, 'route', None, None, 'new', 0)
    session.connect()
    session.disconnect()


def logins(server):
    path = server[2] / 'logins.txt'
    return path.read_text(encoding='utf8').count('password') if path.exists() else 0


def test_an_unknown_server_is_recorded_and_from_then_on_checked(server, settings):
    port, host_key, _folder = server
    connect(port)
    line = settings.read_text(encoding='utf8').strip()
    assert line == f'[127.0.0.1]:{port} ssh-rsa {host_key.get_base64()}'
    connect(port)                                                   # the same key: fine
    assert settings.read_text(encoding='utf8').strip() == line      # recorded once
    assert logins(server) == 2


def test_a_server_with_another_key_is_refused_before_the_password_is_sent(server, settings):
    from bots.exceptions import CommunicationError
    port = server[0]
    other = paramiko.RSAKey.generate(2048)
    settings.write_text(f'[127.0.0.1]:{port} ssh-rsa {other.get_base64()}\n', encoding='utf8')
    with pytest.raises(CommunicationError, match='is not the one recorded'):
        connect(port)
    assert logins(server) == 0


def test_with_refuse_an_unknown_server_is_not_signed_in_to(server, settings):
    from bots import botsglobal
    from bots.exceptions import CommunicationError
    botsglobal.ini.set('settings', 'sftp_unknown_host', 'refuse')
    with pytest.raises(CommunicationError, match='SHA256:'):
        connect(server[0])
    assert logins(server) == 0 and not settings.exists()


def test_with_accept_an_unknown_server_is_used_as_before(server, settings):
    from bots import botsglobal
    botsglobal.ini.set('settings', 'sftp_unknown_host', 'accept')
    connect(server[0])
    assert logins(server) == 1 and not settings.exists()


def test_a_host_key_from_a_user_script_still_wins(server, settings):
    """bots 3: the communication script's hostkey(); then the known_hosts file is not used"""
    from bots import communication
    from bots.exceptions import CommunicationError

    class Script:
        @staticmethod
        def hostkey(channeldict, **kwargs):
            return paramiko.RSAKey.generate(2048)                   # not the server's

    channel = {'idchannel': 'ut_sftp', 'type': 'sftp', 'inorout': 'in', 'host': '127.0.0.1', 'port': server[0],
               'username': 'bots', 'secret': 'botspw', 'keyfile': '', 'parameters': '', 'path': '', 'debug': None}
    session = communication.sftp(channel, 'route', Script, 'ut_sftp', 'new', 0)
    with pytest.raises(CommunicationError, match='is not the one'):
        session.connect()
    assert not settings.exists()

"""SFTP sign-in with a private key file: a key without a passphrase leaves the Password free for a server that asks
for a password after the key (publickey, then password or keyboard-interactive), against a local server
(_sftp_server.py)."""
import os
import subprocess
import sys

import pytest

paramiko = pytest.importorskip('paramiko')

HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def start(botsenv, tmp_path):
    """start(after_key='') starts a local sftp server that knows the public key of tmp_path/'id_rsa'; returns its
    port. sftp_unknown_host is accept (the host key check has its own tests)."""
    from bots import botsglobal
    key = paramiko.RSAKey.generate(2048)
    (tmp_path / 'id_rsa.pub').write_text(f'ssh-rsa {key.get_base64()}\n', encoding='utf8')
    home = tmp_path / 'home'
    home.mkdir()
    processes = []
    botsglobal.ini.set('settings', 'sftp_unknown_host', 'accept')

    def start_server(after_key=''):
        process = subprocess.Popen([sys.executable, os.path.join(HERE, '_sftp_server.py'), str(home), 'bots',
                                    'botspw', str(tmp_path / 'id_rsa.pub'), '', after_key],
                                   stdout=subprocess.PIPE, text=True)
        processes.append(process)
        return int(process.stdout.readline())

    start_server.key = key
    try:
        yield start_server
    finally:
        botsglobal.ini.remove_option('settings', 'sftp_unknown_host')
        for process in processes:
            process.kill()
            process.wait(10)


def write_key(start, path, passphrase=None):
    start.key.write_private_key_file(str(path), password=passphrase)
    return str(path)


def connect(port, keyfile, secret):
    from bots import communication
    channel = {'idchannel': 'ut_sftp', 'type': 'sftp', 'inorout': 'in', 'host': '127.0.0.1', 'port': port,
               'username': 'bots', 'secret': secret, 'keyfile': keyfile, 'parameters': '', 'path': '', 'debug': None}
    session = communication.sftp(channel, 'route', None, None, 'new', 0)
    session.connect()
    session.disconnect()


def logins(tmp_path):
    path = tmp_path / 'logins.txt'
    return [line.split()[0] for line in path.read_text(encoding='utf8').splitlines()] if path.exists() else []


@pytest.mark.parametrize('second', ['password', 'keyboard-interactive'])
def test_a_server_that_demands_the_key_and_then_the_password_gets_both(start, tmp_path, second):
    """a key without a passphrase signs in first, then the Password is sent as the account's password (as bots 3's
    Transport.connect did); keyboard-interactive is answered with it"""
    port = start(after_key=second)
    connect(port, write_key(start, tmp_path / 'id_rsa'), 'botspw')
    methods = logins(tmp_path)
    assert methods[0] == 'publickey' and methods[-1] == second, methods


def test_a_key_without_a_passphrase_and_a_password_set_sends_no_password_when_the_key_is_enough(start, tmp_path):
    port = start()
    connect(port, write_key(start, tmp_path / 'id_rsa'), 'a login password')
    assert set(logins(tmp_path)) == {'publickey'}


def test_a_key_with_a_passphrase_still_takes_the_password_as_passphrase(start, tmp_path):
    port = start()
    connect(port, write_key(start, tmp_path / 'id_rsa', 'key-pass'), 'key-pass')
    assert set(logins(tmp_path)) == {'publickey'}


def test_a_key_with_a_passphrase_on_a_server_that_also_wants_a_password_is_refused_clearly(start, tmp_path):
    """the Password of a channel whose key has a passphrase is that passphrase: there is no password to give"""
    port = start(after_key='password')
    with pytest.raises(paramiko.AuthenticationException, match='asks for a password after the key'):
        connect(port, write_key(start, tmp_path / 'id_rsa', 'key-pass'), 'key-pass')
    assert 'password' not in logins(tmp_path)


def test_a_key_without_a_password_on_a_server_that_also_wants_one_is_refused_clearly(start, tmp_path):
    port = start(after_key='password')
    with pytest.raises(paramiko.AuthenticationException, match='allows password next'):
        connect(port, write_key(start, tmp_path / 'id_rsa'), '')
    assert logins(tmp_path) == ['publickey']

"""TLS context of a channel; private keys for sftp."""
import ssl

import pytest


def comsession(**channel):
    """a channel object without connection"""
    from bots import communication
    session = communication._comsession.__new__(communication._comsession)      # pylint: disable=protected-access
    session.channeldict = dict({'certfile': None, 'keyfile': None}, **channel)
    return session


def test_tls_context_verifies_by_default(botsenv):
    context = comsession().tls_context()
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname is True
    # a channel that has the fields, as read from the database
    context = comsession(verify_cert=1, cafile=None).tls_context()
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname is True


def test_tls_context_without_verification(botsenv):
    context = comsession(verify_cert=0).tls_context()
    assert context.verify_mode == ssl.CERT_NONE and context.check_hostname is False


def test_tls_context_wrong_ca_file_is_an_error(botsenv, tmp_path):
    notacert = tmp_path / 'ca.pem'
    notacert.write_text('this is not a certificate')
    with pytest.raises(ssl.SSLError):
        comsession(cafile=str(notacert)).tls_context()
    with pytest.raises(ssl.SSLError):
        comsession(certfile=str(notacert)).tls_context()      # certfile without keyfile: used as CA file


def test_version_tuple():
    from bots.communication import botslib_version_tuple
    assert botslib_version_tuple('2.0') < botslib_version_tuple('10.1.0')
    assert botslib_version_tuple('3.4.0rc1') == (3, 4, 0)


# ---------------------------------------------------------------- sftp keys

def write_keys(tmp_path):
    """{name: (file, passphrase, name of paramiko class)}: RSA, ECDSA, Ed25519, each with and without passphrase"""
    paramiko = pytest.importorskip('paramiko')
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519
    keys = {}
    for name, key in (('rsa', paramiko.RSAKey.generate(2048)), ('ecdsa', paramiko.ECDSAKey.generate())):
        for passphrase in (None, 'secret'):
            path = str(tmp_path / (name + ('_enc' if passphrase else '')))
            key.write_private_key_file(path, password=passphrase)
            keys[name + ('_enc' if passphrase else '')] = (path, passphrase, key.__class__.__name__)
    for passphrase in (None, 'secret'):
        path = str(tmp_path / ('ed25519' + ('_enc' if passphrase else '')))
        encryption = serialization.BestAvailableEncryption(passphrase.encode()) if passphrase \
            else serialization.NoEncryption()
        with open(path, 'wb') as f:
            f.write(ed25519.Ed25519PrivateKey.generate().private_bytes(
                serialization.Encoding.PEM, serialization.PrivateFormat.OpenSSH, encryption))
        keys['ed25519' + ('_enc' if passphrase else '')] = (path, passphrase, 'Ed25519Key')
    return keys


def test_sftp_private_key_of_any_type(botsenv, tmp_path):
    from bots import communication
    keys = write_keys(tmp_path)
    assert len(keys) == 6
    for name, (path, passphrase, classname) in keys.items():
        key = communication.load_private_key(path, passphrase)
        assert key.__class__.__name__ == classname, name
    # the type given by a user script ('privatekey' returns file, type, passphrase) is a hint, not a demand
    path, passphrase, classname = keys['ed25519']
    assert communication.load_private_key(path, passphrase, 'RSA').__class__.__name__ == classname
    assert communication.load_private_key(keys['rsa'][0], '', 'DSA').__class__.__name__ == 'RSAKey'


def test_sftp_private_key_errors_are_clear(botsenv, tmp_path):
    from bots import communication
    from bots.exceptions import CommunicationError
    keys = write_keys(tmp_path)
    with pytest.raises(CommunicationError, match='no passphrase'):
        communication.load_private_key(keys['rsa_enc'][0], None)
    with pytest.raises(CommunicationError, match='can not read private key'):
        communication.load_private_key(keys['ed25519_enc'][0], 'wrong')
    notakey = tmp_path / 'notakey'
    notakey.write_text('this is not a key')
    with pytest.raises(CommunicationError, match='can not read private key'):
        communication.load_private_key(str(notakey), None)


# ---------------------------------------------------------------- found with a real ftp/sftp service

def test_ftps_upload_does_not_depend_on_the_server_closing_tls():
    """a server that does not answer 'close notify' after an upload: no error, and a short wait"""
    import ssl
    from unittest import mock
    from bots import communication
    conn = mock.create_autospec(ssl.SSLSocket, instance=True)
    conn.gettimeout.return_value = 20
    conn.unwrap.side_effect = TimeoutError('The read operation timed out')
    communication.end_tls_of_data_connection(conn)
    conn.settimeout.assert_called_once_with(2)
    conn.unwrap.assert_called_once_with()
    # a connection without TLS is left alone
    plain = mock.Mock()
    communication.end_tls_of_data_connection(plain)
    assert not plain.method_calls
    assert issubclass(communication.Ftp_tls_implicit, communication.Ftp_tls)


def test_sftp_new_file_is_not_opened_for_append():
    """append asks the server for the size of the file; a server that gives none for a new file got 0 bytes"""
    from unittest import mock
    from bots import communication
    channel = communication.sftp.__new__(communication.sftp)
    channel.session = mock.Mock()
    channel.session.stat.side_effect = IOError('No such file')
    assert channel.open_mode('new.edi', 'a') == 'w'
    channel.session.stat.side_effect = None
    assert channel.open_mode('there.edi', 'a') == 'a'
    channel.session.stat.reset_mock()
    assert channel.open_mode('any.edi', 'w') == 'w'
    channel.session.stat.assert_not_called()

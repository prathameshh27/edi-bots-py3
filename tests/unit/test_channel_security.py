"""TLS context of a channel; private keys for sftp; outgoing file names."""
import os
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


# ---------------------------------------------------------------- outgoing file names

def outgoing_ta(channel, **fields):
    """a file to send by channel, with the given values (eg botskey); returns its transaction"""
    from bots import botslib
    from bots.botsconfig import FILEOUT, OK
    ta = botslib.NewTransaction(status=FILEOUT, statust=OK, tochannel=channel, **fields)
    ta.update(filename=str(ta.idta))
    with botslib.opendata_bin(str(ta.idta), 'wb') as data:
        data.write(b'content')
    return ta


def formatted(mask, **fields):
    from bots import botslib, communication
    session = communication._comsession.__new__(communication._comsession)      # pylint: disable=protected-access
    session.channeldict = {'idchannel': 'ut_names'}
    session.userscript = None
    return session.filename_formatter(mask, botslib.OldTransaction(outgoing_ta('ut_names', **fields).idta))


@pytest.mark.parametrize('botskey', ['../evil', r'..\evil', 'a/b', r'a\b', '/etc/evil', r'C:\evil', '..', 'C:'])
def test_a_value_in_an_outgoing_file_name_is_not_a_folder(botsenv, botskey):
    """bots 3: values were put in the file name as they are; {botskey} of '../x' wrote outside the channel's
    folder, 'C:' made a name on another drive"""
    from bots.exceptions import CommunicationOutError
    with pytest.raises(CommunicationOutError, match='outside the folder of the channel|is not a folder'):
        formatted('{botskey}', botskey=botskey)


def test_path_text_of_the_mask_itself_is_kept(botsenv):
    assert formatted('{botskey}.edi', botskey='4500012345') == '4500012345.edi'
    assert formatted('out/{botskey}.edi', botskey='123') == 'out/123.edi'
    assert formatted('../archive/{botskey}.edi', botskey='123') == '../archive/123.edi'
    assert formatted('/data/out/{editype}_{botskey}.edi', botskey='123', editype='x12') == '/data/out/x12_123.edi'
    assert formatted('{datetime:%Y/%m}/{botskey}.edi', botskey='123').endswith('/123.edi')
    assert formatted('{botskey}..edi', botskey='a') == 'a..edi'
    assert formatted('{botskey}', botskey='a.b') == 'a.b'


def test_a_value_in_the_http_parameters_may_have_a_slash(botsenv):
    """the parameters of a http channel are no file name"""
    from bots import botslib, communication
    session = communication.http.__new__(communication.http)
    session.channeldict = {'idchannel': 'ut_names', 'parameters': 'order={botskey}'}
    session.userscript = None
    session.params = {}
    session.get_params(botslib.OldTransaction(outgoing_ta('ut_names', botskey='2026/001').idta))
    assert session.params == {'order': '2026/001'}


def send_status(ta):
    from bots import botslib
    from bots.botsconfig import EXTERNOUT
    rows = [dict(row) for row in botslib.query('SELECT statust, errortext FROM ta WHERE parent=%(idta)s AND '
                                               'status=%(status)s', {'idta': ta.idta, 'status': EXTERNOUT})]
    return rows[0]['statust'], rows[0]['errortext']


def test_a_file_channel_does_not_write_outside_its_folder(botsenv, tmp_path):
    from bots import communication
    from bots.botsconfig import DONE, ERROR
    outdir = tmp_path / 'partner' / 'out'
    session = communication.file.__new__(communication.file)
    session.channeldict = {'idchannel': 'ut_names_file', 'path': str(outdir), 'filename': '{botskey}.edi',
                           'syslock': False, 'mdnchannel': ''}
    session.userscript = None
    session.rootidta = outgoing_ta('ut_names_file').idta
    bad = outgoing_ta('ut_names_file', botskey='../../evil')
    good = outgoing_ta('ut_names_file', botskey='ok')
    session.outcommunicate()
    assert sorted(os.listdir(tmp_path)) == ['partner'] and sorted(os.listdir(outdir)) == ['ok.edi']
    statust, errortext = send_status(bad)
    assert statust == ERROR and '{botskey}' in errortext and '../../evil' in errortext
    assert send_status(good)[0] == DONE


@pytest.mark.parametrize('kind', ['ftp', 'sftp', 'communicationscript'])
def test_other_channels_do_not_send_outside_their_folder(botsenv, tmp_path, kind):
    from unittest import mock
    from bots import communication
    from bots.botsconfig import DONE, ERROR
    channel = 'ut_names_' + kind
    session = getattr(communication, kind).__new__(getattr(communication, kind))
    session.channeldict = {'idchannel': channel, 'path': str(tmp_path), 'filename': '{botskey}.edi',
                           'mdnchannel': '', 'ftpbinary': True, 'remove': False}
    session.userscript = session.scriptname = None
    session.session = mock.MagicMock()
    session.dirpath = '/out'
    session.rootidta = outgoing_ta(channel).idta
    bad = outgoing_ta(channel, botskey=r'..\evil')
    good = outgoing_ta(channel, botskey='ok')
    session.outcommunicate()
    statust, errortext = send_status(bad)
    assert statust == ERROR and r'..\evil' in errortext
    assert send_status(good)[0] == DONE
    sent = [str(call) for call in session.session.mock_calls if 'evil' in str(call)]
    assert not sent
    if kind == 'communicationscript':
        assert os.listdir(tmp_path) == ['ok.edi']


@pytest.mark.parametrize('kind', ['ftp', 'sftp'])
def test_a_file_name_that_can_not_be_made_is_an_error_of_that_file(botsenv, kind):
    """bots 3: the error of the file name was lost in an UnboundLocalError ('tofilename'); the file was marked
    done but not sent, the next files were not sent at all"""
    from unittest import mock
    from bots import communication
    from bots.botsconfig import ERROR
    channel = 'ut_names_mask_' + kind
    session = getattr(communication, kind).__new__(getattr(communication, kind))
    session.channeldict = {'idchannel': channel, 'filename': '{nosuchfield}.edi', 'mdnchannel': '',
                           'ftpbinary': True}
    session.userscript = session.scriptname = None
    session.session = mock.MagicMock()
    session.dirpath = '/out'
    session.rootidta = outgoing_ta(channel).idta
    first, second = outgoing_ta(channel), outgoing_ta(channel)
    session.outcommunicate()
    assert send_status(first)[0] == send_status(second)[0] == ERROR
    assert 'nosuchfield' in send_status(second)[1]


def test_the_name_a_communication_script_gives_is_used_as_it_is(botsenv):
    import types as pytypes
    from bots import botslib, communication
    session = communication._comsession.__new__(communication._comsession)      # pylint: disable=protected-access
    session.channeldict = {'idchannel': 'ut_names'}
    session.userscript = pytypes.SimpleNamespace(filename=lambda channeldict, filename, ta: ta.botskey + '.edi')
    session.scriptname = 'ut_names'
    ta = botslib.OldTransaction(outgoing_ta('ut_names', botskey='2026/001').idta)
    assert session.filename_formatter('{botskey}', ta) == '2026/001.edi'

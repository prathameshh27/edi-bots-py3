"""ftp channel against a local ftp server (pyftpdlib, started by the test).

ASCII mode is the default of a channel. What is expected in ASCII mode is what bots 3.2.0 did for files it
could receive (line end CRLF -> LF, last line gets a line end, a CR on its own is kept); files with
non-ASCII bytes, which bots 3.2.0 refused, are received with their bytes unchanged.
"""
import os
import threading

import pytest

pyftpdlib = pytest.importorskip('pyftpdlib')

SEP = os.linesep.encode()       # the server sends the line ends of its platform as CRLF
REMOTE = {                      # name on server: (content on server, expected after ASCII receive)
    'ascii.edi': (b"UNB+UNOA:2+S+R+260101:1200+1'" + SEP + b"UNZ+0+1'" + SEP, b"UNB+UNOA:2+S+R+260101:1200+1'\nUNZ+0+1'\n"),
    'latin1.edi': ('café français'.encode('latin-1') + SEP, 'café français\n'.encode('latin-1')),
    'utf8.edi': ('café € 10'.encode('utf-8') + SEP, 'café € 10\n'.encode('utf-8')),
    'barecr.edi': (b'one\rtwo' + SEP + b'three' + SEP, b'one\rtwo\nthree\n'),
    'nolineend.edi': (b'one' + SEP + b'last', b'one\nlast\n'),
    'big.edi': ((b'x' * 79 + SEP) * 5000, (b'x' * 79 + b'\n') * 5000),
}


@pytest.fixture
def ftpserver(tmp_path):
    """yields (port, home directory of user 'bots' with password 'botspw')"""
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer

    home = tmp_path / 'ftphome'
    home.mkdir()
    authorizer = DummyAuthorizer()
    authorizer.add_user('bots', 'botspw', str(home), perm='elradfmwMT')

    class Handler(FTPHandler):
        pass
    Handler.authorizer = authorizer
    server = FTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, kwargs={'timeout': 0.2}, daemon=True)
    thread.start()
    yield server.socket.getsockname()[1], str(home)
    server.close_all()
    thread.join(5)


def ftp_channel(idchannel, inorout, port, path, **more):
    return dict(idchannel=idchannel, inorout=inorout, type='ftp', host='127.0.0.1', port=port, username='bots',
                secret='botspw', path=path, filename='*.edi', **more)


def run_route(botsrun, name, fromchannel, tochannel):
    botsrun.configure(channels=[fromchannel, tochannel],
                      routes=[dict(idroute=name, seq=1, active=True, fromchannel=fromchannel['idchannel'],
                                   tochannel=tochannel['idchannel'], translateind=2)])
    code = botsrun.engine()
    return code, botsrun.result()


def delivered(directory):
    """{content of file} of the files in directory"""
    found = []
    for name in os.listdir(directory):
        with open(os.path.join(directory, name), 'rb') as f:
            found.append(f.read())
    return sorted(found)


def fill(home, subdir):
    directory = os.path.join(home, subdir)
    os.makedirs(directory)
    for name, (content, _expected) in REMOTE.items():
        with open(os.path.join(directory, name), 'wb') as f:
            f.write(content)
    return directory


def test_receive_ascii_mode(botsrun, ftpserver):
    port, home = ftpserver
    remote = fill(home, 'inbox')
    os.makedirs(os.path.join(remote, 'directory.edi'))     # a directory that matches the file mask is skipped
    out = botsrun.path('out')
    code, result = run_route(
        botsrun, 'ftpin', ftp_channel('ftp_in', 'in', port, 'inbox', ftpbinary=False, remove=True),
        dict(idchannel='file_out', inorout='out', type='file', path=out, filename='*.edi'))
    assert code == 0 and result['report']['lasterror'] == 0 and result['report']['processerrors'] == 0, (
        botsrun.root, result['errors'])
    assert delivered(out) == sorted(expected for _content, expected in REMOTE.values())
    assert os.listdir(remote) == ['directory.edi'], 'received files are removed from the server'


def test_receive_binary_mode(botsrun, ftpserver):
    port, home = ftpserver
    fill(home, 'inbox')
    out = botsrun.path('out')
    code, result = run_route(
        botsrun, 'ftpin', ftp_channel('ftp_in', 'in', port, 'inbox', ftpbinary=True, remove=True),
        dict(idchannel='file_out', inorout='out', type='file', path=out, filename='*.edi'))
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    assert delivered(out) == sorted(content for content, _expected in REMOTE.values())


@pytest.mark.parametrize('binary', [False, True])
def test_send(botsrun, ftpserver, binary):
    port, home = ftpserver
    src = botsrun.path('src')
    content = 'café €\none\rtwo\nlast\n'.encode('utf-8')
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(content)
    code, result = run_route(
        botsrun, 'ftpout', dict(idchannel='file_in', inorout='in', type='file', path=src, filename='*.edi'),
        ftp_channel('ftp_out', 'out', port, 'outbox', ftpbinary=binary))
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    # ASCII: lines are sent with CRLF; the server stores the line ends of its platform
    expected = content if binary else content.replace(b'\n', SEP)
    assert delivered(os.path.join(home, 'outbox')) == [expected]

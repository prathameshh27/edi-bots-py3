"""Channels with TLS against local servers with a self-signed certificate: https and ftps.

Per protocol three channels to the same server:
- certificate is verified (default), CA not known: no connection;
- certificate is verified, 'CA certificate file' is set: works;
- 'Verify server certificate' off (as channels of an upgraded bots 3 database): works.
"""
import datetime
import http.server
import ipaddress
import os
import ssl
import threading

import pytest

pytest.importorskip('requests')
pytest.importorskip('cryptography')

PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'UNZ+0+1'"
CASES = {'strict': {}, 'ca': {'cafile': None}, 'off': {'verify_cert': False}}       # cafile is filled in


def make_certificate(directory, name):
    """self-signed certificate for 127.0.0.1 / localhost; returns (certfile, keyfile)"""
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, name)])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(subject).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=30))
            .add_extension(x509.SubjectAlternativeName(
                [x509.DNSName('localhost'), x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]), critical=False)
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(key, hashes.SHA256()))
    certfile, keyfile = os.path.join(directory, name + '.crt'), os.path.join(directory, name + '.key')
    with open(certfile, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(keyfile, 'wb') as f:
        f.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL,
                                  serialization.NoEncryption()))
    return certfile, keyfile


@pytest.fixture
def certificate(tmp_path):
    return make_certificate(str(tmp_path), 'server')


def outcome(botsrun, routes):
    """run the routes one by one; returns {route: True if no error}"""
    found = {}
    for route in routes:
        botsrun.engine(route)
        report = botsrun.result()['report']
        found[route] = report['lasterror'] == 0 and report['processerrors'] == 0
    return found


def test_https(botsrun, certificate):
    certfile, keyfile = certificate
    received = []

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):          # pylint: disable=invalid-name
            self.rfile.read(int(self.headers.get('Content-Length', 0)))
            received.append(self.path)
            self.send_response(200)
            self.send_header('Content-Length', '0')
            self.end_headers()

        def log_message(self, format, *args):       # pylint: disable=redefined-builtin
            pass

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile, keyfile)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        channels, routes = [], []
        for name, fields in CASES.items():
            src = botsrun.path('src_' + name)
            with open(os.path.join(src, 'order.edi'), 'wb') as f:
                f.write(PAYLOAD)
            fields = dict(fields, **({'cafile': certfile} if 'cafile' in fields else {}))
            channels += [dict(idchannel='in_' + name, inorout='in', type='file', path=src, filename='*.edi'),
                         dict(idchannel='https_' + name, inorout='out', type='https', host='127.0.0.1',
                              port=server.server_address[1], path='api/' + name, **fields)]
            routes.append(dict(idroute=name, seq=1, active=True, fromchannel='in_' + name, tochannel='https_' + name,
                               translateind=2))
        botsrun.configure(channels=channels, routes=routes)
        assert outcome(botsrun, CASES) == {'strict': False, 'ca': True, 'off': True}, botsrun.root
        assert sorted(received) == ['/api/ca', '/api/off']
    finally:
        server.shutdown()
        server.server_close()
        thread.join(5)


def test_ftps(botsrun, certificate, tmp_path):
    pytest.importorskip('pyftpdlib')
    pytest.importorskip('OpenSSL')
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import TLS_FTPHandler
    from pyftpdlib.servers import FTPServer

    certfile, keyfile = certificate
    home = tmp_path / 'ftphome'
    home.mkdir()
    authorizer = DummyAuthorizer()
    authorizer.add_user('bots', 'botspw', str(home), perm='elradfmwMT')

    class Handler(TLS_FTPHandler):
        pass
    Handler.authorizer = authorizer
    Handler.certfile, Handler.keyfile = certfile, keyfile
    Handler.tls_control_required = Handler.tls_data_required = True
    server = FTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, kwargs={'timeout': 0.2}, daemon=True)
    thread.start()
    try:
        channels, routes = [], []
        for name, fields in CASES.items():
            os.makedirs(home / name)
            with open(home / name / 'order.edi', 'wb') as f:
                f.write(PAYLOAD)
            fields = dict(fields, **({'cafile': certfile} if 'cafile' in fields else {}))
            channels += [dict(idchannel='ftps_' + name, inorout='in', type='ftps', host='127.0.0.1',
                              port=server.socket.getsockname()[1], username='bots', secret='botspw', path=name,
                              filename='*.edi', ftpbinary=True, remove=True, **fields),
                         dict(idchannel='out_' + name, inorout='out', type='file', path=botsrun.path('out_' + name),
                              filename='*.edi')]
            routes.append(dict(idroute=name, seq=1, active=True, fromchannel='ftps_' + name, tochannel='out_' + name,
                               translateind=2))
        botsrun.configure(channels=channels, routes=routes)
        assert outcome(botsrun, CASES) == {'strict': False, 'ca': True, 'off': True}, botsrun.root
        assert [len(os.listdir(botsrun.path('out_' + name))) for name in CASES] == [0, 1, 1]
        assert os.listdir(home / 'strict') == ['order.edi'], 'nothing is taken from a server that is not trusted'
    finally:
        server.close_all()
        thread.join(5)

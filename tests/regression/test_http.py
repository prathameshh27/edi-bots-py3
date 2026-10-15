"""http channel against a local http server (started by the test)."""
import http.server
import os
import threading
import urllib.parse

import pytest

pytest.importorskip('requests')

PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'UNZ+0+1'"


@pytest.fixture
def httpserver():
    """yields (port, list of received requests, list of contents the server gives on GET)"""
    received, queue = [], []

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):          # pylint: disable=invalid-name
            url = urllib.parse.urlsplit(self.path)
            body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
            received.append(dict(method='POST', path=url.path, query=dict(urllib.parse.parse_qsl(url.query)),
                                 headers=dict(self.headers.items()), body=body))
            self.send_response(200)
            self.send_header('Content-Length', '0')
            self.end_headers()

        def do_GET(self):           # pylint: disable=invalid-name
            url = urllib.parse.urlsplit(self.path)
            received.append(dict(method='GET', path=url.path, query=dict(urllib.parse.parse_qsl(url.query))))
            content = queue.pop(0) if queue else b''
            self.send_response(200)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def log_message(self, format, *args):       # pylint: disable=redefined-builtin
            pass

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server.server_address[1], received, queue
    server.shutdown()
    server.server_close()
    thread.join(5)


def http_channel(idchannel, inorout, port, path, **more):
    return dict(idchannel=idchannel, inorout=inorout, type='http', host='127.0.0.1', port=port, path=path, **more)


def test_send_two_channels_in_one_run(botsrun, httpserver):
    """each channel sends its own parameters and headers; each file goes to the url of the channel"""
    port, received, _queue = httpserver
    src_a, src_b = botsrun.path('src_a'), botsrun.path('src_b')
    for directory, names in ((src_a, ('a1.edi', 'a2.edi')), (src_b, ('b1.edi',))):
        for name in names:
            with open(os.path.join(directory, name), 'wb') as f:
                f.write(PAYLOAD + name.encode())
    botsrun.configure(
        channels=[
            dict(idchannel='in_a', inorout='in', type='file', path=src_a, filename='*.edi'),
            dict(idchannel='in_b', inorout='in', type='file', path=src_b, filename='*.edi'),
            # debug 2 logs the request and the response
            http_channel('http_a', 'out', port, 'api/a', filename='{infile}', sendmdn='attachment', debug=2,
                         parameters='token=abc=%3D&partner=A B'),
            http_channel('http_b', 'out', port, 'api/b', parameters='single=1'),
        ],
        routes=[dict(idroute='route_a', seq=1, active=True, fromchannel='in_a', tochannel='http_a', translateind=2),
                dict(idroute='route_b', seq=1, active=True, fromchannel='in_b', tochannel='http_b', translateind=2)])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])

    posts = sorted(received, key=lambda request: request['body'])
    assert [(post['path'], post['body']) for post in posts] == [
        ('/api/a', PAYLOAD + b'a1.edi'), ('/api/a', PAYLOAD + b'a2.edi'), ('/api/b', PAYLOAD + b'b1.edi')]
    assert posts[0]['query'] == posts[1]['query'] == {'token': 'abc==', 'partner': 'A B'}
    assert posts[2]['query'] == {'single': '1'}
    assert posts[0]['headers']['Content-Disposition'] == 'attachment; filename=a1.edi'
    assert posts[1]['headers']['Content-Disposition'] == 'attachment; filename=a2.edi'
    assert posts[2]['headers']['Content-Disposition'] == 'inline'


def test_receive(botsrun, httpserver):
    port, received, queue = httpserver
    queue.append(PAYLOAD)
    out = botsrun.path('out')
    botsrun.configure(
        channels=[http_channel('http_in', 'in', port, 'api/orders', parameters='since=20260101'),
                  dict(idchannel='file_out', inorout='out', type='file', path=out, filename='*.edi')],
        routes=[dict(idroute='httpin', seq=1, active=True, fromchannel='http_in', tochannel='file_out', translateind=2)])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    assert received[0] == dict(method='GET', path='/api/orders', query={'since': '20260101'})
    files = os.listdir(out)
    assert len(files) == 1
    with open(os.path.join(out, files[0]), 'rb') as f:
        assert f.read() == PAYLOAD

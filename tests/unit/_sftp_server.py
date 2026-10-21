"""A small SFTP server for the tests (paramiko's server side), run in a process of its own:

    python _sftp_server.py <home folder> <user> <password> [<public key file>] [<host key file>]

prints its port, then serves the home folder until it is killed. Log in with the password, or with the key.
With a host key file (a private RSA key) the server shows that key, else a new one; every login is written to
<home folder>/../logins.txt, so a test can see whether a password was sent."""
import os
import socket
import sys
import threading

import paramiko
from paramiko import SFTPAttributes, SFTPHandle, SFTPServer, SFTPServerInterface
from paramiko.sftp import SFTP_FAILURE, SFTP_NO_SUCH_FILE, SFTP_OK

HOME, USER, PASSWORD = sys.argv[1:4]
PUBLIC_KEY = open(sys.argv[4], encoding='utf8').read().split()[1] if len(sys.argv) > 4 and sys.argv[4] else None
HOST_KEY_FILE = sys.argv[5] if len(sys.argv) > 5 else None
LOGINS = os.path.join(os.path.dirname(os.path.abspath(HOME)), 'logins.txt')


class Server(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        with open(LOGINS, 'a', encoding='utf8') as log:
            log.write(f'password {username}\n')
        return paramiko.AUTH_SUCCESSFUL if (username, password) == (USER, PASSWORD) else paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_SUCCESSFUL if username == USER and key.get_base64() == PUBLIC_KEY else paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password,publickey'

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED


class Handle(SFTPHandle):
    def stat(self):
        return SFTPAttributes.from_stat(os.fstat(self.readfile.fileno()))


def errors(function):
    def wrapper(*args):
        try:
            return function(*args)
        except FileNotFoundError:
            return SFTP_NO_SUCH_FILE
        except OSError:
            return SFTP_FAILURE
    return wrapper


class Files(SFTPServerInterface):
    def real(self, path):
        return os.path.join(HOME, self.canonicalize(path).lstrip('/'))

    def canonicalize(self, path):
        return '/' + '/'.join(part for part in os.path.normpath('/' + path).replace('\\', '/').split('/') if part)

    @errors
    def list_folder(self, path):
        folder = self.real(path)
        listing = []
        for name in os.listdir(folder):
            attributes = SFTPAttributes.from_stat(os.stat(os.path.join(folder, name)))
            attributes.filename = name
            listing.append(attributes)
        return listing

    @errors
    def stat(self, path):
        return SFTPAttributes.from_stat(os.stat(self.real(path)))

    lstat = stat

    @errors
    def open(self, path, flags, attr):
        mode = 'ab' if flags & os.O_APPEND else ('r+b' if flags & (os.O_WRONLY | os.O_RDWR) else 'rb')
        if flags & os.O_TRUNC or (flags & os.O_CREAT and not os.path.exists(self.real(path))):
            mode = 'wb'
        handle = Handle(flags)
        handle.readfile = handle.writefile = open(self.real(path), mode)
        return handle

    @errors
    def remove(self, path):
        os.remove(self.real(path))
        return SFTP_OK

    @errors
    def rename(self, oldpath, newpath):
        os.rename(self.real(oldpath), self.real(newpath))
        return SFTP_OK

    @errors
    def mkdir(self, path, attr):
        os.mkdir(self.real(path))
        return SFTP_OK


def serve(client, host_key):
    transport = paramiko.Transport(client)
    transport.add_server_key(host_key)
    transport.set_subsystem_handler('sftp', SFTPServer, Files)
    transport.start_server(server=Server())
    while transport.is_active():
        transport.join(1)


host_key = paramiko.RSAKey(filename=HOST_KEY_FILE) if HOST_KEY_FILE else paramiko.RSAKey.generate(2048)
listener = socket.socket()
listener.bind(('127.0.0.1', 0))
listener.listen(5)
print(listener.getsockname()[1], flush=True)
while True:
    connection, _address = listener.accept()
    threading.Thread(target=serve, args=(connection, host_key), daemon=True).start()

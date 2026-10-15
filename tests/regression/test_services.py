"""bots-jobqueueserver and bots-dirmonitor as running processes: a file dropped in a watched directory is processed.

The daemons are started from source; a small script named `bots-engine` on PATH stands for the installed
console script.
"""
import os
import re
import socket
import subprocess
import sys
import time

import pytest

if os.name == 'posix':
    pytest.importorskip('pyinotify')
else:
    pytest.importorskip('win32file')

PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'UNZ+0+1'"
START = "import sys; sys.argv[0] = 'bots-%(name)s'; from bots.%(name)s import start; start()"


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class Services:
    """job queue and directory monitor of one environment"""

    def __init__(self, botsrun, dirmonitor_sections=''):
        self.botsrun = botsrun
        self.procs = {}
        self.logs = {}
        # bots.ini: job queue on, with a port of its own; sections for the directory monitor
        ini = os.path.join(botsrun.envdir, 'config', 'bots.ini')
        with open(ini, encoding='utf8') as f:
            txt = f.read()
        start = txt.index('[jobqueue]')
        end = txt.index('\n[', start)
        section = txt[start:end]
        section, count1 = re.subn(r'(?m)^enabled\s*=.*$', 'enabled = True', section)
        section, count2 = re.subn(r'(?m)^port\s*=.*$', 'port = %s\nstopwait = 20' % free_port(), section)
        assert (count1, count2) == (1, 1), section
        txt = txt[:start] + section + txt[end:]
        with open(ini, 'w', encoding='utf8') as f:
            f.write(txt + '\n' + dirmonitor_sections)
        # the console script bots-engine
        bindir = botsrun.path('bin')
        engine = "import sys; sys.argv[0] = 'bots-engine'; from bots.engine import start; start()"
        if os.name == 'nt':
            with open(os.path.join(bindir, 'bots-engine.cmd'), 'w', encoding='utf8') as f:
                f.write('@"%s" -c "%s" %%*\n' % (sys.executable, engine))
        else:
            script = os.path.join(bindir, 'bots-engine')
            with open(script, 'w', encoding='utf8') as f:
                f.write('#!/bin/sh\nexec "%s" -c "%s" "$@"\n' % (sys.executable, engine))
            os.chmod(script, 0o755)
        self.env = dict(botsrun.env, PATH=bindir + os.pathsep + os.environ.get('PATH', ''))

    def start(self, name):
        self.logs[name] = os.path.join(self.botsrun.root, name + '.out')
        with open(self.logs[name], 'ab') as out:
            self.procs[name] = subprocess.Popen(
                [sys.executable, '-c', START % {'name': name}], env=self.env, stdout=out, stderr=subprocess.STDOUT)

    def run(self, name, *args):
        return subprocess.run([sys.executable, '-c', START % {'name': name}] + list(args), env=self.env,
                              capture_output=True, text=True)

    def output(self, name):
        """what the daemon wrote: its own output and its log file"""
        text = ''
        logname = name.replace('server', '')
        logfile = os.path.join(self.botsrun.envdir, 'botssys', 'logging', logname, logname + '.log')
        for path in (logfile,):
            if path and os.path.exists(path):
                with open(path, encoding='utf8', errors='replace') as f:
                    text += f.read()
        return text

    def wait_for(self, condition, seconds=60):
        end = time.time() + seconds
        while time.time() < end:
            if condition():
                return True
            time.sleep(0.5)
        return False

    def quiet(self, seconds=6):
        """wait until every job is finished and no job was added for some seconds; returns the number of jobs"""
        last, since = None, time.time()
        end = time.time() + 120
        while time.time() < end:
            log = self.output('jobqueueserver')
            now = (log.count('Added job'), log.count('Finished job'))
            if now != last:
                last, since = now, time.time()
            elif now[0] == now[1] and time.time() - since >= seconds:
                return now[0]
            time.sleep(0.5)
        raise AssertionError('jobs keep coming: %s' % self.output('jobqueueserver')[-2000:])

    def stop(self):
        for proc in self.procs.values():
            if proc.poll() is None:
                proc.terminate()
        for proc in self.procs.values():
            try:
                proc.wait(30)
            except subprocess.TimeoutExpired:
                proc.kill()


def drop(directory, name):
    with open(os.path.join(directory, name), 'wb') as f:
        f.write(PAYLOAD)


def test_file_in_watched_directory_is_processed(botsrun):
    src, sub, out = botsrun.path('src'), botsrun.path('src', 'sub'), botsrun.path('out')
    src2, out2 = botsrun.path('src2'), botsrun.path('out2')
    services = Services(botsrun, (
        # dirmonitor1: as in the bots.ini that is installed, nothing set. dirmonitor7: a recursive watch.
        '[dirmonitor7]\npath = %s\nrecursive = True\nfilemask = *.edi\nroute = watched\n' % src))
    botsrun.configure(
        channels=[dict(idchannel='w_in', inorout='in', type='file', path=sub, filename='*.edi', remove=True),
                  dict(idchannel='w_in_top', inorout='in', type='file', path=src, filename='*.edi', remove=True),
                  dict(idchannel='w_out', inorout='out', type='file', path=out, filename='{infile}'),
                  dict(idchannel='r_in', inorout='in', type='file', path=src2, filename='*.edi', remove=True),
                  dict(idchannel='r_out', inorout='out', type='file', path=out2, filename='{infile}')],
        routes=[dict(idroute='watched', seq=1, active=True, fromchannel='w_in_top', tochannel='w_out', translateind=2),
                dict(idroute='watched', seq=2, active=True, fromchannel='w_in', tochannel='w_out', translateind=2),
                # a route with 'dirmonitor' ticked, but not active yet
                dict(idroute='viaroute', seq=1, active=False, dirmonitor=True, fromchannel='r_in', tochannel='r_out',
                     translateind=2)])
    try:
        services.start('jobqueueserver')
        assert services.wait_for(lambda: 'Listening xmlrpc' in services.output('jobqueueserver'), 30), \
            services.output('jobqueueserver')
        services.start('dirmonitor')
        assert services.wait_for(lambda: 'Started.' in services.output('dirmonitor'), 30), services.output('dirmonitor')
        assert services.procs['dirmonitor'].poll() is None, services.output('dirmonitor')

        # a file in the watched directory, and one in a sub-directory of it
        drop(src, 'top.edi')
        assert services.wait_for(lambda: len(os.listdir(out)) == 1), (
            services.output('dirmonitor')[-2000:], services.output('jobqueueserver')[-2000:])
        drop(sub, 'deeper.edi')
        assert services.wait_for(lambda: len(os.listdir(out)) == 2), (
            services.output('dirmonitor')[-2000:], services.output('jobqueueserver')[-2000:])
        # a file that does not match the mask starts nothing
        jobs = services.quiet()
        drop(src, 'notes.txt')
        time.sleep(6)
        assert services.output('jobqueueserver').count('Added job') == jobs

        # reload: the route that is made active now is watched after the reload
        botsrun.side('activate', 'viaroute')
        assert services.run('dirmonitor', '--reload').returncode == 0
        assert services.wait_for(lambda: services.output('dirmonitor').count('Started.') == 2, 40), \
            services.output('dirmonitor')[-3000:]
        drop(src2, 'route.edi')
        assert services.wait_for(lambda: len(os.listdir(out2)) == 1), (
            services.output('dirmonitor')[-2000:], services.output('jobqueueserver')[-2000:])
        # and the watch from bots.ini still works
        drop(src, 'again.edi')
        assert services.wait_for(lambda: len(os.listdir(out)) == 3), services.output('dirmonitor')[-2000:]
    finally:
        services.stop()
    assert 'Invalid task' not in services.output('jobqueueserver')

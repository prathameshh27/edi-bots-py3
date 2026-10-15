"""bots-engine: start and exit; the console scripts bots-configure and bots-plugoutindex."""
import io
import json
import os
import re
import socket
import subprocess
import sys
import textwrap
import time
import zipfile

PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'UNZ+0+1'"
SCRIPT = "import sys; sys.argv[0] = '%(name)s'; from bots.%(module)s import %(function)s; %(function)s()"


def console_script(env, name, module, function, *args):
    return subprocess.run(
        [sys.executable, '-c', SCRIPT % {'name': name, 'module': module, 'function': function}] + list(args),
        env=env, capture_output=True, text=True, encoding='utf8', errors='replace')


def engine_log(botsrun):
    with open(os.path.join(botsrun.root, 'engine.log'), encoding='utf8', errors='replace') as f:
        return f.read()


def set_ini(botsrun, section, text):
    """add lines to a section of bots.ini"""
    ini = os.path.join(botsrun.envdir, 'config', 'bots.ini')
    with open(ini, encoding='utf8') as f:
        txt = f.read()
    assert txt.count('\n[%s]' % section) == 1
    with open(ini, 'w', encoding='utf8') as f:
        f.write(txt.replace('\n[%s]' % section, '\n[%s]\n%s' % (section, text)))


def simple_route(botsrun, name='simple', **route):
    src, out = botsrun.path('src_' + name), botsrun.path('out_' + name)
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(PAYLOAD)
    botsrun.configure(
        channels=[dict(idchannel=name + '_in', inorout='in', type='file', path=src, filename='*.edi', remove=True),
                  dict(idchannel=name + '_out', inorout='out', type='file', path=out, filename='{infile}')],
        routes=[dict(idroute=name, seq=1, active=True, fromchannel=name + '_in', tochannel=name + '_out',
                     translateind=2, **route)])
    return src, out


# ---------------------------------------------------------------- console scripts

def test_bots_configure_makes_an_environment(botsrun):
    """(writes its arguments to a dict; in python 3.13+ writing to locals() is lost)"""
    envdir = os.path.join(botsrun.root, 'made_by_configure')
    env = dict(botsrun.env)
    env.pop('BOTS_CONFIG_DIR', None)
    done = console_script(env, 'bots-configure', 'configure', 'start', 'botsenv_path=' + envdir, '--yes')
    assert done.returncode == 0, done.stderr[-1500:]
    assert os.path.isfile(os.path.join(envdir, 'config', 'bots.ini'))
    assert os.path.isfile(os.path.join(envdir, 'botssys', 'sqlitedb', 'botsdb'))
    assert 'Bots Environment' in done.stderr and os.path.join(envdir, 'config') in done.stderr


def test_bots_plugoutindex_writes_the_configuration(botsrun):
    simple_route(botsrun, 'indexed')
    done = console_script(botsrun.env, 'bots-plugoutindex', 'plugmanager', 'plugoutindex')
    assert done.returncode == 0, done.stderr[-1500:]
    index = os.path.join(botsrun.envdir, 'usersys', 'index.json')
    with open(index, encoding='utf8') as f:
        text = f.read()
    json.loads(text)
    assert 'indexed_in' in text and 'indexed_out' in text


# ---------------------------------------------------------------- engine start

def test_second_engine_tells_why_it_does_not_run(botsrun):
    with open(os.path.join(botsrun.envdir, 'config', 'bots.ini'), encoding='utf8') as f:
        port = int(re.search(r'(?m)^port\s*=\s*(\d+)', f.read()).group(1))
    with socket.socket() as busy:
        busy.bind(('127.0.0.1', port))
        busy.listen(1)
        assert botsrun.engine() == 3
    assert 'another bots-engine is running' in engine_log(botsrun)


def test_unknown_route_is_reported_readable(botsrun):
    botsrun.engine('nosuchroute')
    log = engine_log(botsrun)
    assert 'There is no (active) route "nosuchroute".' in log
    assert '%(route)s' not in log


# ---------------------------------------------------------------- engine exit

def test_engine_ends_when_a_thread_is_left_running(botsrun):
    """a thread that does not stop (started by a user script or a library) can not keep the engine alive"""
    set_ini(botsrun, 'settings', 'maxsecondsexit = 3')
    _src, out = simple_route(botsrun, 'threaded')
    directory = os.path.join(botsrun.envdir, 'usersys', 'routescripts')
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, 'threaded.py'), 'w', encoding='utf8') as f:
        f.write(textwrap.dedent('''
            import threading, time

            def keeps_running():
                time.sleep(600)

            def start(routedict):
                threading.Thread(target=keeps_running, name='left-by-script').start()
            '''))
    start = time.time()
    proc = subprocess.Popen([sys.executable, '-c', SCRIPT % {'name': 'bots-engine', 'module': 'engine',
                                                             'function': 'start'}, '--new'],
                            env=botsrun.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        output = proc.communicate(timeout=120)[0].decode('utf8', errors='replace')
    finally:
        if proc.poll() is None:
            proc.kill()
    assert proc.returncode == 0, output[-2000:]
    assert time.time() - start < 100
    assert 'still running' in output and 'left-by-script' in output and 'keeps_running' in output
    assert os.listdir(out) == ['order.edi'], 'the work is done'
    # the database is not left locked: the next run is a normal run
    assert botsrun.engine() == 0
    assert 'database is locked' not in engine_log(botsrun)


def test_log_per_run_can_replace_an_existing_log(botsrun):
    """log_when = report: the log gets the number of the run; a file with that name can be there"""
    set_ini(botsrun, 'settings', 'log_when = report')
    simple_route(botsrun, 'logged')
    logdir = os.path.join(botsrun.envdir, 'botssys', 'logging', 'engine')
    os.makedirs(logdir, exist_ok=True)
    for number in range(1, 60):
        with open(os.path.join(logdir, str(number)), 'w', encoding='utf8') as f:
            f.write('old log')
    assert botsrun.engine() == 0, engine_log(botsrun)[-2000:]
    assert 'FileExistsError' not in engine_log(botsrun)
    replaced = [name for name in os.listdir(logdir) if name.isdigit()
                and open(os.path.join(logdir, name), encoding='utf8', errors='replace').read() != 'old log']
    assert len(replaced) == 1, sorted(os.listdir(logdir))


# ---------------------------------------------------------------- zip

def test_two_route_parts_to_one_zip_channel(botsrun):
    """each file is zipped once, also when an earlier part of the route left its files for the same channel"""
    src_a, src_b, out = botsrun.path('src_a'), botsrun.path('src_b'), botsrun.path('out')
    for directory, name in ((src_a, 'a.edi'), (src_b, 'b.edi')):
        with open(os.path.join(directory, name), 'wb') as f:
            f.write(PAYLOAD + name.encode())
    botsrun.configure(
        channels=[dict(idchannel='z_in_a', inorout='in', type='file', path=src_a, filename='*.edi'),
                  dict(idchannel='z_in_b', inorout='in', type='file', path=src_b, filename='*.edi'),
                  dict(idchannel='z_out', inorout='out', type='file', path=out, filename='{infile}.zip')],
        routes=[dict(idroute='zipped', seq=1, active=True, fromchannel='z_in_a', tochannel='z_out', translateind=2,
                     zip_outgoing=1, defer=True),
                dict(idroute='zipped', seq=2, active=True, fromchannel='z_in_b', tochannel='z_out', translateind=2,
                     zip_outgoing=1)])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    found = {}
    for name in os.listdir(out):
        with zipfile.ZipFile(os.path.join(out, name)) as archive:
            members = archive.namelist()
            assert len(members) == 1, (name, members)
            content = archive.read(members[0])
        assert not zipfile.is_zipfile(io.BytesIO(content)), '%s is a zip in a zip' % name
        found[name] = content
    assert found == {'a.edi.zip': PAYLOAD + b'a.edi', 'b.edi.zip': PAYLOAD + b'b.edi'}

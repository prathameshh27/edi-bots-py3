"""bots-updatedb on PostgreSQL 17 / MariaDB 11.4 / MySQL 8.4 in throwaway docker containers (not run by pytest).

For each server: a genuine bots 3.2.0 database (dumps/: made by bots 3.2.0 itself, with three official plugins,
run history and three users) and an empty database. Checks: --check, refusal without confirmation, upgrade,
column lengths, number of rows kept, and one file through bots-engine.

Needs: docker; python drivers psycopg, psycopg2 (for pg2) and mysqlclient.
usage: python dbmatrix.py <workdir> [pg|pg2|maria|mysql ...]        (prints the results as json; also <workdir>/dbmatrix.json)
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO, DUMPS, WORK = os.path.dirname(os.path.dirname(HERE)), os.path.join(HERE, 'dumps'), os.path.abspath(sys.argv[1])
WANTED = sys.argv[2:] or ['pg', 'pg2', 'maria', 'mysql']
os.makedirs(WORK, exist_ok=True)
SIDE = os.path.join(REPO, 'tests', 'regression', '_side.py')
UPDATEDB = "import sys; sys.argv[0] = 'bots-updatedb'; from bots.botsupdatedb import start; start()"
ENGINE = "import sys; sys.argv[0] = 'bots-engine'; from bots.engine import start; start()"
PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'UNZ+0+1'"
PW = 'botsstab'
SERVERS = {
    'pg': dict(image='postgres:17', port=55432, inner=5432, env=['POSTGRES_PASSWORD=' + PW], dump='pg17_bots320.sql',
               engine='django.db.backends.postgresql', user='postgres'),
    # the same, with psycopg2 as the only driver (psycopg made unimportable)
    'pg2': dict(image='postgres:17', port=55433, inner=5432, env=['POSTGRES_PASSWORD=' + PW], dump='pg17_bots320.sql',
                engine='django.db.backends.postgresql', user='postgres'),
    'maria': dict(image='mariadb:11.4', port=53306, inner=3306, env=['MARIADB_ROOT_PASSWORD=' + PW], dump='maria_bots320.sql',
                  engine='django.db.backends.mysql', user='root', client='mariadb'),
    'mysql': dict(image='mysql:8.4', port=53307, inner=3306, env=['MYSQL_ROOT_PASSWORD=' + PW], dump='mysql84_bots320.sql',
                  engine='django.db.backends.mysql', user='root', client='mysql'),
}


def sh(*args, check=True, **kw):
    proc = subprocess.run(list(args), capture_output=True, text=True, encoding='utf8', errors='replace', **kw)
    if check and proc.returncode:
        raise RuntimeError('%s\n%s' % (' '.join(args), (proc.stdout + proc.stderr)[-2000:]))
    return proc


def sql(key, database, statement, check=True):
    srv, name = SERVERS[key], 'botsstab-' + key
    if key.startswith('pg'):
        return sh('docker', 'exec', name, 'psql', '-U', 'postgres', '-d', database, '-At', '-c', statement, check=check).stdout
    return sh('docker', 'exec', name, srv['client'], '-uroot', '-p' + PW, '-N', '-B', database, '-e', statement, check=check).stdout


def start_server(key):
    srv, name = SERVERS[key], 'botsstab-' + key
    sh('docker', 'rm', '-f', name, check=False)
    args = ['docker', 'run', '-d', '--name', name, '-p', '127.0.0.1:%s:%s' % (srv['port'], srv['inner'])]
    for env in srv['env']:
        args += ['-e', env]
    sh(*args, srv['image'])
    for _ in range(90):
        time.sleep(2)
        probe = sql(key, 'postgres' if key.startswith('pg') else 'mysql', 'SELECT 1', check=False)
        if probe.strip() == '1':
            try:
                socket.create_connection(('127.0.0.1', srv['port']), timeout=2).close()
                time.sleep(3)
                return
            except OSError:
                pass
    raise RuntimeError('server %s did not start' % key)


def make_database(key, database, dump=None):
    name, srv = 'botsstab-' + key, SERVERS[key]
    if key.startswith('pg'):
        sql(key, 'postgres', 'CREATE DATABASE %s' % database)
    else:
        sql(key, 'mysql', 'CREATE DATABASE %s CHARACTER SET utf8mb4' % database)
    if dump:
        sh('docker', 'cp', os.path.join(DUMPS, dump), name + ':/tmp/dump.sql')
        if key.startswith('pg'):
            sh('docker', 'exec', name, 'psql', '-U', 'postgres', '-d', database, '-q', '-v', 'ON_ERROR_STOP=1', '-f', '/tmp/dump.sql')
        else:
            sh('docker', 'exec', name, 'sh', '-c', '%s -uroot -p%s %s < /tmp/dump.sql' % (srv['client'], PW, database))


def make_env(key, database):
    envdir = os.path.join(WORK, '%s_%s' % (key, database))
    shutil.rmtree(envdir, ignore_errors=True)
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    env.pop('BOTS_CONFIG_DIR', None)
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
    sh(sys.executable, SIDE, 'create', envdir, str(port), env=env)
    srv = SERVERS[key]
    options = {} if key.startswith('pg') else {'charset': 'utf8mb4'}
    with open(os.path.join(envdir, 'config', 'settings.py'), 'a', encoding='utf8') as f:
        f.write('\nDATABASES = {"default": %r}\n' % dict(
            ENGINE=srv['engine'], NAME=database, USER=srv['user'], PASSWORD=PW, HOST='127.0.0.1', PORT=str(srv['port']),
            OPTIONS=options))
    # not acceptance-test mode: real counters and clock
    ini = os.path.join(envdir, 'config', 'bots.ini')
    with open(ini, encoding='utf8') as f:
        txt = f.read().replace('runacceptancetest = True', 'runacceptancetest = False')
    with open(ini, 'w', encoding='utf8') as f:
        f.write(txt)
    env['BOTS_CONFIG_DIR'] = os.path.join(envdir, 'config')
    if key == 'pg2':
        stub = os.path.join(envdir, 'nopsycopg3')
        os.makedirs(stub)
        with open(os.path.join(stub, 'psycopg.py'), 'w', encoding='utf8') as f:
            f.write("raise ImportError('psycopg (version 3) is hidden in this test')\n")
        env['PYTHONPATH'] = stub
    return envdir, env


def updatedb(env, *args):
    proc = subprocess.run([sys.executable, '-c', UPDATEDB] + list(args), env=env, capture_output=True, text=True,
                          encoding='utf8', errors='replace')
    return proc.returncode, proc.stdout + proc.stderr


def passthrough(envdir, env, name):
    src, out = os.path.join(envdir, 'src_' + name), os.path.join(envdir, 'out_' + name)
    os.makedirs(src), os.makedirs(out)
    with open(os.path.join(src, 'order.edi'), 'wb') as f:
        f.write(PAYLOAD)
    spec = os.path.join(envdir, 'spec.json')
    with open(spec, 'w', encoding='utf8') as f:
        json.dump(dict(
            channels=[dict(idchannel=name + '_in', inorout='in', type='file', path=src, filename='*.edi'),
                      dict(idchannel=name + '_out', inorout='out', type='file', path=out, filename='*.edi')],
            routes=[dict(idroute=name, seq=1, active=True, fromchannel=name + '_in', tochannel=name + '_out', translateind=2)]), f)
    sh(sys.executable, SIDE, 'configure', spec, env=env)
    proc = subprocess.run([sys.executable, '-c', ENGINE, '--new', name], env=env, capture_output=True)
    with open(os.path.join(envdir, 'engine.log'), 'wb') as f:
        f.write(proc.stdout + proc.stderr)
    return proc.returncode, os.listdir(out)


def draw(env, envdir, processes=4, count=150):
    """several processes draw from one new counter: (all numbers distinct and complete, row[0] works, errors)"""
    results = [os.path.join(envdir, 'draw%s.json' % nr) for nr in range(processes)]
    procs = [subprocess.Popen([sys.executable, SIDE, 'draw', 'dbmatrix_concurrent', str(count), result], env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE) for result in results]
    errors = [proc.communicate()[1].decode(errors='replace')[-300:] for proc in procs if proc.wait() or True]
    numbers, by_position = [], []
    for result in results:
        if os.path.exists(result):
            with open(result, encoding='utf8') as f:
                drawn = json.load(f)
            numbers += drawn['numbers']
            by_position.append(drawn['by_position'])
    return (sorted(numbers) == list(range(1, processes * count + 1)), by_position,
            [error for proc, error in zip(procs, errors) if proc.returncode])


def widths(key, database):
    schema = "current_schema()" if key.startswith('pg') else "DATABASE()"
    rows = sql(key, database,
               "SELECT table_name, column_name, character_maximum_length FROM information_schema.columns "
               "WHERE table_schema = %s AND table_name IN ('ta','uniek','persist') "
               "AND column_name IN ('divtext','reference','botskey','rsrv1','rsrv5','domein') ORDER BY 1,2" % schema)
    sep = '|' if key.startswith('pg') else '\t'
    return ' '.join('%s.%s=%s' % tuple(line.split(sep)) for line in rows.splitlines() if line.strip())


def count(key, database, table):
    return sql(key, database, 'SELECT COUNT(*) FROM %s' % table).strip()


results = {}
for key in WANTED:
    res = results[key] = {}
    try:
        start_server(key)
        # ---- genuine bots 3.2.0 database
        make_database(key, 'bots320', SERVERS[key]['dump'])
        envdir, env = make_env(key, 'bots320')
        res['3.2.0 before'] = dict(widths=widths(key, 'bots320'),
                                   rows=dict((t, count(key, 'bots320', t)) for t in ('ta', 'routes', 'channel', 'auth_user', 'uniek')))
        code, text = updatedb(env, '--check')
        res['3.2.0 check'] = (code, [line for line in text.splitlines() if line.strip()][-9:])
        code, text = updatedb(env)
        res['3.2.0 without confirmation'] = (code, text.strip().splitlines()[-1:])
        code, text = updatedb(env, '--yes-i-have-a-backup')
        res['3.2.0 upgrade'] = (code, [line for line in text.splitlines() if 'Applying' not in line and line.strip()][-14:])
        code, text = updatedb(env, '--check')
        res['3.2.0 check after'] = (code, text.strip().splitlines()[-1:])
        res['3.2.0 after'] = dict(widths=widths(key, 'bots320'),
                                  rows=dict((t, count(key, 'bots320', t)) for t in ('ta', 'routes', 'channel', 'auth_user', 'uniek')))
        res['3.2.0 engine'] = passthrough(envdir, env, 'up')
        res['3.2.0 counters'] = draw(env, envdir)
        # ---- empty database
        make_database(key, 'botsnew')
        envdir, env = make_env(key, 'botsnew')
        code, text = updatedb(env, '--check')
        res['empty check'] = (code, text.strip().splitlines()[-3:])
        code, text = updatedb(env)
        res['empty create'] = (code, [line for line in text.splitlines() if 'Applying' not in line and line.strip()][-6:])
        code, text = updatedb(env, '--check')
        res['empty check after'] = (code, text.strip().splitlines()[-1:])
        res['empty widths'] = widths(key, 'botsnew')
        res['empty engine'] = passthrough(envdir, env, 'new')
    except Exception as exc:
        res['ERROR'] = '%s: %s' % (exc.__class__.__name__, exc)
    finally:
        sh('docker', 'rm', '-f', 'botsstab-' + key, check=False)

with open(os.path.join(WORK, 'dbmatrix.json'), 'w', encoding='utf8') as f:
    json.dump(results, f, indent=1)
print(json.dumps(results, indent=1))

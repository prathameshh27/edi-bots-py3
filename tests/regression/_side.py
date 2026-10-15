"""Helper of test_plugins.py; runs in its own process inside one Bots environment.

usage: python _side.py create  <envdir> <port>
       python _side.py load    <plugin.zip> <golden.json> <result.json>     (BOTS_CONFIG_DIR set)
       python _side.py collect <result.json>                                (BOTS_CONFIG_DIR set)
       python _side.py configure <spec.json>                                (BOTS_CONFIG_DIR set)
       python _side.py draw <domain> <count> <result.json>                  (BOTS_CONFIG_DIR set)
"""
import hashlib
import json
import os
import re
import sys
import traceback


def create(envdir, port):
    """New environment in acceptance-test mode (frozen clock) with a private single-instance port."""
    from bots import botsinit
    botsinit.initbotsenv(botsenv_path=envdir, interactive=False)
    ini = os.path.join(envdir, 'config', 'bots.ini')
    with open(ini, encoding='utf8') as f:
        txt = f.read()
    txt, n1 = re.subn(r'(?m)^runacceptancetest\s*=.*$', 'runacceptancetest = True', txt)
    txt, n2 = re.subn(r'(?m)^port\s*=\s*28081\s*$', 'port = %s' % port, txt)
    assert (n1, n2) == (1, 1), (n1, n2)
    with open(ini, 'w', encoding='utf8', newline='\n') as f:
        f.write(txt)
    on_server(envdir)


def on_server(envdir):
    """BOTS_TEST_DATABASE set: the environment gets a new database on that server (tests/servers.py)"""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import servers
    srv = servers.server()
    if srv is None:
        return
    name = servers.create_database(srv)
    with open(os.path.join(envdir, 'config', 'settings.py'), 'a', encoding='utf8') as f:
        f.write(servers.settings_block(srv, name))
    with open(os.path.join(envdir, 'testdatabase.txt'), 'w', encoding='utf8') as f:
        f.write(name)
    os.environ['BOTS_CONFIG_DIR'] = os.path.join(envdir, 'config')
    from bots import botsinit, botsupdatedb
    botsinit.generalinit()
    code = botsupdatedb.update(backup_confirmed=True, out=lambda text: None)
    assert code == 0, 'tables not made on the test database'


def init():
    from bots import botsinit, botsglobal
    botsinit.generalinit()
    botsglobal.logger = botsinit.initenginelogging('regression')
    botsinit.connect()
    return botsglobal


def tree(base):
    res = {}
    for dirpath, _dirs, files in os.walk(base):
        for name in files:
            full = os.path.join(dirpath, name)
            with open(full, 'rb') as f:
                res[os.path.relpath(full, base).replace(os.sep, '/')] = hashlib.sha256(f.read()).hexdigest()
    return res


def load(plugin, golden_file, result_file):
    init()
    from bots import models, pluglib
    result = {'load_ok': False, 'load_error': ''}
    try:
        pluglib.read_plugin(plugin)
        result['load_ok'] = True
    except Exception:
        result['load_error'] = traceback.format_exc()
    if result['load_ok']:
        # plugin readers import routes inactive; set the flags the plugin author stored
        with open(golden_file, encoding='utf8') as f:
            for idroute, seq, active, _notindefaultrun in json.load(f)['routes']:
                models.routes.objects.filter(idroute=idroute, seq=seq).update(active=active)
    with open(result_file, 'w', encoding='utf8') as f:
        json.dump(result, f, indent=1)


def configure(spec_file):
    """Create partners, channels and routes through the ORM.
    spec (json): {"partners": [{...}], "channels": [{...}], "chanpar": [{...}], "routes": [{...}],
    "translate": [{...}]}"""
    init()
    from bots import models
    with open(spec_file, encoding='utf8') as f:
        spec = json.load(f)
    for key, model in (('partners', models.partner), ('channels', models.channel),
                       ('chanpar', models.chanpar), ('routes', models.routes), ('translate', models.translate)):
        for item in spec.get(key, []):
            # foreign keys are given by their key value: use the attribute name (fromchannel -> fromchannel_id)
            values = dict((model._meta.get_field(k).attname, v) for k, v in item.items())
            model(**values).save()


def collect(result_file):
    botsglobal = init()
    from bots import botslib
    from bots.botsconfig import ERROR
    with open(result_file, encoding='utf8') as f:
        result = json.load(f)
    keys = ('status', 'lastreceived', 'lasterror', 'lastdone', 'lastok', 'lastopen', 'send', 'processerrors', 'filesize')
    rows = list(botslib.query('SELECT * FROM report ORDER BY idta DESC'))
    result['report'] = dict((k, rows[0][k]) for k in keys) if rows else None
    result['files'] = sorted(
        [os.path.basename((row['infilename'] or '').replace('\\', '/')), row['statust']]
        for row in botslib.query('SELECT infilename, statust FROM filereport'))
    result['errors'] = sorted(set(
        row['errortext'] for row in botslib.query('SELECT errortext FROM ta WHERE statust=%(st)s', {'st': ERROR})
        if row['errortext']))
    result['outdir'] = os.path.join(botsglobal.ini.get('directories', 'botssys'), 'outfile')
    result['outfiles'] = tree(result['outdir'])
    with open(result_file, 'w', encoding='utf8') as f:
        json.dump(result, f, indent=1)


def draw(domain, count, result_file):
    """Draw numbers from a counter, as the engine does; and read a row by name and by position."""
    init()
    from bots import botslib
    numbers = [botslib.unique(domain) for _ in range(int(count))]
    row = list(botslib.query('SELECT nummer, domein FROM uniek WHERE domein=%(domein)s', {'domain': domain, 'domein': domain}))[0]
    try:
        by_position = (row[0], row[1]) == (row['nummer'], row['domein'])
    except KeyError:
        by_position = False         # MySQLdb gives a plain dict (also in bots 3)
    with open(result_file, 'w', encoding='utf8') as f:
        json.dump({'numbers': numbers, 'by_position': by_position}, f)


def activate(idroute):
    """Set a route active (as a user does in the web interface)."""
    init()
    from bots import models
    for route in models.routes.objects.filter(idroute=idroute):
        route.active = True
        route.save()


def sql(*statements):
    """Change the database as given (to bring it in a state a test needs)."""
    init()
    from bots import botslib
    for statement in statements:
        botslib.changeq(statement)


if __name__ == '__main__':
    {'create': create, 'load': load, 'configure': configure, 'collect': collect, 'draw': draw,
     'activate': activate, 'sql': sql}[sys.argv[1]](*sys.argv[2:])

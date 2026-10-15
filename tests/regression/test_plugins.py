"""Regression suite: the official Bots plugins must give the same result as Bots 3.2.0.

For every plugin under plugins/ a fresh environment is created, the plugin is loaded through pluglib, the engine is
run once (acceptance-test mode: frozen clock, counters start at 1) and the outcome is compared with golden/, which
holds what Bots 3.2.0 on Python 2.7 did with the same plugin: run counters, status per input file, and every output
file byte for byte. See README.md for how the reference data was made.

    pytest tests/regression/test_plugins.py            # all plugins, a few minutes
    pytest tests/regression/test_plugins.py -k x12     # a selection
"""
import datetime
import difflib
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SIDE = os.path.join(HERE, '_side.py')
ENGINE = "import sys; sys.argv[0] = 'bots-engine'; from bots.engine import start; start()"

# Plugins that do not match Bots 3.2.0 yet: name -> reason. strict: the test fails when it starts to pass,
# so the entry has to be removed together with the fix.
XFAIL = {
}

# Differences from the 3.2.0 reference that are accepted: name -> list of (description, normaliser) applied to both
# the reference and the new output before comparing; or files left out of the byte comparison, with the reason.
def json_content(data):
    """json: Bots 3.2.0 (python 2) writes the fields of an object in arbitrary order; compare the content."""
    if data[:1] in (b'{', b'['):
        try:
            return json.dumps(json.loads(data.decode('utf-8')), sort_keys=True, ensure_ascii=False).encode('utf-8')
        except ValueError:
            pass
    return data


def wall_clock_dtm(data):
    """a mapping that writes the current time itself (not frozen by acceptance-test mode)"""
    return re.sub(rb"DTM\+137:\d{12}:203'", b"DTM+137:<now>:203'", data)


NORMALISE = {'*': [json_content], 'edifact_ordersdesadvinvoic_20111124': [wall_clock_dtm]}
# Bots 2 era plugins whose output contains the real run date (written before acceptance-test mode existed).
# The reference run was made on 2026-10-12; that date and today's are masked before comparing.
RUN_DATE = {
    'edifact_orders2csv_20130224', 'edifact_ordersdesadvinvoic_20111124', 'tradacoms_orders2xml_20111211',
    'edifact_json2invoic_20111211',
}
REFERENCE_DATE = datetime.date(2026, 10, 12)


def mask_run_date(data, day):
    for fmt in ('%Y%m%d', '%y%m%d'):
        data = data.replace(day.strftime(fmt).encode('ascii'), b'<rundate>')
    return data
REFERENCE_FROM_PLUGIN = {}
SKIP_FILES = {
    # these mappings loop over a Python set; the record order under Python 2 cannot be reproduced
    'demo_working_with_partners_20140312': {
        'demo_work_with_partners/outbound_856/PARTNER1_20130123_1.x12',
        'demo_work_with_partners/outbound_856/PARTNER2_20130123_1.x12',
    },
    'x12toxml_supplier_version850-856-810-997_20130711': {'x12_demo/outbound_856/856_1.x12', 'x12_demo/outbound_856/856_2.x12'},
}
REPORT_OVERRIDE = {}
REFERENCE_FAILS = set()


def cases():
    return list(_cases())


def _cases():
    for label in sorted(os.listdir(os.path.join(HERE, 'plugins'))):
        for fname in sorted(os.listdir(os.path.join(HERE, 'plugins', label))):
            name = fname[:-4]
            marks = [pytest.mark.xfail(reason=XFAIL[name], strict=True)] if name in XFAIL else []
            yield pytest.param(label, name, id='%s/%s' % (label, name), marks=marks)


class _Path(str):
    def __truediv__(self, other):
        return _Path(os.path.join(self, other))


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def run(args, env, log, timeout=600):
    proc = subprocess.run([sys.executable] + args, env=env, capture_output=True, timeout=timeout)
    with open(log, 'wb') as f:
        f.write(proc.stdout + b'\n--- stderr ---\n' + proc.stderr)
    return proc.returncode


def normalise(name, data, reference):
    for func in NORMALISE['*'] + NORMALISE.get(name, []):
        data = func(data)
    if name in RUN_DATE:
        data = mask_run_date(data, REFERENCE_DATE if reference else datetime.date.today())
    return data


def show_diff(old, new):
    old, new = old.decode('latin-1'), new.decode('latin-1')
    if old.count('\n') < 3:
        old, new = re.sub(r"(?<=['~])", '\n', old), re.sub(r"(?<=['~])", '\n', new)
    return '\n'.join(list(difflib.unified_diff(old.splitlines(), new.splitlines(), 'bots 3.2.0', 'new', lineterm='', n=0))[:20])

def temp_base():
    """
    Where the directories of the tests are made: <project>/.temp/tests if the project (the directory
    bots-new-stable is in) has a directory .temp, or $BOTS_TEST_TEMP; else the temp directory of the system.
    """
    base = os.environ.get('BOTS_TEST_TEMP')
    if not base:
        here = os.path.dirname(os.path.abspath(__file__))
        project = os.path.dirname(os.path.dirname(os.path.dirname(here)))
        if not os.path.isdir(os.path.join(project, '.temp')):
            return None
        base = os.path.join(project, '.temp', 'tests')
    os.makedirs(base, exist_ok=True)
    return base



@pytest.fixture
def workdir():
    """Short private directory (deep pytest tmp paths exceed the Windows path limit); kept when the test fails."""
    path = tempfile.mkdtemp(prefix='botsrt', dir=temp_base())
    yield path


@pytest.fixture(autouse=True)
def _cleanup(request, workdir):
    yield
    report = getattr(request.node, 'rep_call', None)
    if report is None or report.passed or report.skipped:      # skipped = expected failure
        shutil.rmtree(workdir, ignore_errors=True)


@pytest.mark.parametrize('label, name', cases())
def test_plugin(label, name, workdir):
    tmp_path = _Path(workdir)
    plugin = os.path.join(HERE, 'plugins', label, name + '.zip')
    gdir = os.path.join(HERE, 'golden', label, name)
    golden_file = os.path.join(gdir, 'golden.json')
    with open(golden_file, encoding='utf8') as f:
        golden = json.load(f)
    envdir = str(tmp_path / 'env')
    result_file = str(tmp_path / 'result.json')
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    for key in ('BOTS_CONFIG_DIR', 'BOTSENV', 'DJANGO_SETTINGS_MODULE'):
        env.pop(key, None)

    assert run([SIDE, 'create', envdir, str(free_port())], env, str(tmp_path / 'create.log')) == 0, 'environment not created'
    env['BOTS_CONFIG_DIR'] = os.path.join(envdir, 'config')
    assert run([SIDE, 'load', plugin, golden_file, result_file], env, str(tmp_path / 'load.log')) == 0
    with open(result_file, encoding='utf8') as f:
        loaded = json.load(f)
    assert loaded['load_ok'], 'plugin does not load:\n' + loaded['load_error'][-1500:]

    for _attempt in range(3):
        code = run(['-c', ENGINE, '--new'], env, str(tmp_path / 'engine.log'))
        if code != 3:       # 3 = another engine holds the port
            break
    assert code in (0, 2), 'engine exit code %s, see %s' % (code, tmp_path / 'engine.log')
    assert run([SIDE, 'collect', result_file], env, str(tmp_path / 'collect.log')) == 0
    with open(result_file, encoding='utf8') as f:
        new = json.load(f)

    if name in REFERENCE_FAILS:
        return
    expected_report = dict(golden['report'], **REPORT_OVERRIDE.get(name, {}))
    counters = ('status', 'lastreceived', 'lasterror', 'lastdone', 'lastok', 'lastopen', 'send', 'processerrors')
    assert dict((k, new['report'][k]) for k in counters) == dict((k, expected_report[k]) for k in counters), \
        'run counters differ; errors: %s' % [e.strip().splitlines()[-1][:300] for e in new['errors']][:4]

    skip = SKIP_FILES.get(name, set())
    assert sorted(new['outfiles']) == sorted(golden['outfiles']), 'set of output files differs'
    problems = []
    for rel in sorted(golden['outfiles']):
        if rel in skip:
            continue
        if rel in REFERENCE_FROM_PLUGIN.get(name, ()):
            reference = os.path.join(os.path.dirname(new['outdir']), 'infile', 'outfile', *rel.split('/'))
        else:
            reference = os.path.join(gdir, 'outfile', *rel.split('/'))
        with open(reference, 'rb') as f:
            old_data = normalise(name, f.read(), reference=True)
        with open(os.path.join(new['outdir'], *rel.split('/')), 'rb') as f:
            new_data = normalise(name, f.read(), reference=False)
        if hashlib.sha256(old_data).digest() != hashlib.sha256(new_data).digest():
            problems.append('%s\n%s' % (rel, show_diff(old_data, new_data)))
    assert not problems, '%d output file(s) differ from Bots 3.2.0:\n\n%s' % (len(problems), '\n\n'.join(problems[:5]))

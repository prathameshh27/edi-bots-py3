"""pytest hooks and fixtures for the regression suite."""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SIDE = os.path.join(HERE, '_side.py')
ENGINE = "import sys; sys.argv[0] = 'bots-engine'; from bots.engine import start; start()"
UPDATEDB = "import sys; sys.argv[0] = 'bots-updatedb'; from bots.botsupdatedb import start; start()"


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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make the outcome of the test body available to fixtures (the work directory is kept when a test fails)."""
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        item.rep_call = report


class Env:
    """A bots environment in a short temporary directory, driven through subprocesses."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix='botsrm', dir=temp_base())
        self.envdir = os.path.join(self.root, 'env')
        self.env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
        for key in ('BOTS_CONFIG_DIR', 'BOTSENV', 'DJANGO_SETTINGS_MODULE'):
            self.env.pop(key, None)
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        self.side('create', self.envdir, str(port))
        self.env['BOTS_CONFIG_DIR'] = os.path.join(self.envdir, 'config')

    def path(self, *parts):
        path = os.path.join(self.root, *parts)
        os.makedirs(path, exist_ok=True)
        return path

    def side(self, *args):
        proc = subprocess.run([sys.executable, SIDE] + list(args), env=self.env, capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr[-1500:]

    def configure(self, **spec):
        spec_file = os.path.join(self.root, 'spec.json')
        with open(spec_file, 'w', encoding='utf8') as f:
            json.dump(spec, f)
        self.side('configure', spec_file)

    def engine(self, *args):
        proc = subprocess.run([sys.executable, '-c', ENGINE, '--new'] + list(args), env=self.env, capture_output=True)
        with open(os.path.join(self.root, 'engine.log'), 'wb') as f:
            f.write(proc.stdout + proc.stderr)
        return proc.returncode

    def updatedb(self, *args):
        """run bots-updatedb; returns (exit code, output)"""
        proc = subprocess.run([sys.executable, '-c', UPDATEDB] + list(args), env=self.env, capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr

    @property
    def database(self):
        return os.path.join(self.envdir, 'botssys', 'sqlitedb', 'botsdb')

    def result(self):
        result_file = os.path.join(self.root, 'result.json')
        with open(result_file, 'w', encoding='utf8') as f:
            json.dump({}, f)
        self.side('collect', result_file)
        with open(result_file, encoding='utf8') as f:
            return json.load(f)


@pytest.fixture
def botsrun(request):
    env = Env()
    yield env
    report = getattr(request.node, 'rep_call', None)
    if report is None or report.passed or report.skipped:
        shutil.rmtree(env.root, ignore_errors=True)


@pytest.fixture(scope='session', autouse=True)
def _test_databases_on_a_server():
    """with BOTS_TEST_DATABASE: drop the databases the tests made on the server (tests/servers.py)"""
    sys.path.insert(0, os.path.dirname(HERE))
    import servers
    yield
    for srv in (servers.server(), servers.server('BOTS_TEST_CHANNEL_DATABASE')):
        if srv is not None:
            servers.drop_databases(srv)

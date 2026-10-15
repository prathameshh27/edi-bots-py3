"""Unit tests that need an initialised Bots: one private environment per test session.

The environment (config, botssys with an empty sqlite database, usersys) is created in a temporary directory by
Bots itself; nothing is read from or written to the user's own ~/.bots.
"""
import os
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # helpers.py


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


@pytest.fixture(scope='session', autouse=True)
def botsenv():
    """Initialise Bots on a fresh environment; yields the environment directory."""
    envdir = tempfile.mkdtemp(prefix='botsut', dir=temp_base())
    os.environ.pop('BOTSENV', None)
    from bots import botsinit, botsglobal
    botsinit.initbotsenv(botsenv_path=envdir, interactive=False)
    os.environ['BOTS_CONFIG_DIR'] = os.path.join(envdir, 'config')
    botsinit.generalinit()
    botsglobal.logger = botsinit.initenginelogging('unittest')
    botsinit.connect()
    yield envdir
    import django.db
    django.db.connections.close_all()
    botsglobal.db.close()
    for handler in list(botsglobal.logger.handlers):
        handler.close()
        botsglobal.logger.removeHandler(handler)
    shutil.rmtree(envdir, ignore_errors=True)

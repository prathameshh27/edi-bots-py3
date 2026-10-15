"""Reading bots.ini, locating the config directory, decoding mail headers."""
import os
import subprocess
import sys

import pytest


def test_botsconfig_get_defaults():
    from bots.botsinit import BotsConfig
    from bots.exceptions import BotsConfigError
    ini = BotsConfig()
    ini.read_string("[s]\nfilled = x\nempty =\n")
    assert ini.get('s', 'filled') == 'x'
    assert ini.get('s', 'empty', 'dflt') == 'dflt'
    assert ini.get('s', 'empty') == ''
    assert ini.get('s', 'missing', '') == ''              # an explicit default, also '', is never an error
    assert ini.get('s', 'missing', None) is None
    with pytest.raises(BotsConfigError):
        ini.get('s', 'missing')
    assert ini.getint('s', 'missing', 7) == 7 and ini.getboolean('s', 'missing', True) is True


def test_section_or_option_twice_in_bots_ini_is_read_as_python2_did():
    """a bots.ini of bots 3 with a section twice (python 2 accepts it) must not stop bots: last value counts"""
    from bots.botsinit import BotsConfig
    ini = BotsConfig()
    ini.read_string("[directories]\nusersys = a\nbotssys = b\n[settings]\nx = 1\nx = 2\n[directories]\nusersys = c\n")
    assert ini.get('directories', 'usersys') == 'c' and ini.get('directories', 'botssys') == 'b'
    assert ini.get('settings', 'x') == '2'


SCRIPT = """
import os, sys
from bots import botsinit, botsglobal
botsinit.generalinit(*sys.argv[1:])
botsglobal.logger = botsinit.initenginelogging('ut')
print('CONFIG=' + botsglobal.ini.get('directories', 'config'))
print('LOG_WHEN=' + botsglobal.ini.get('settings', 'log_when'))
print('TRIGGER=' + botsglobal.ini.get('dirmonitor', 'trigger'))
print('VALIDATE=' + botsglobal.ini.get('webserver', 'validate_email_address', 'not set'))
print('USERSYS=' + botsglobal.ini.get('directories', 'usersysabs'))
"""


@pytest.fixture
def otherenv(tmp_path):
    """A second environment, created by a separate process (Django settings are per process)."""
    envdir = str(tmp_path / 'e')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for key in ('BOTS_CONFIG_DIR', 'BOTSENV', 'DJANGO_SETTINGS_MODULE'):
        env.pop(key, None)
    subprocess.run(
        [sys.executable, '-c', 'import sys; from bots import botsinit; botsinit.initbotsenv(botsenv_path=sys.argv[1], interactive=False)', envdir],
        env=env, check=True, capture_output=True)
    return envdir, env


def run_init(cwd, env, *args):
    proc = subprocess.run([sys.executable, '-c', SCRIPT] + list(args), cwd=cwd, env=env, capture_output=True, text=True)
    values = dict(line.split('=', 1) for line in proc.stdout.splitlines() if '=' in line and line.split('=')[0].isupper())
    return proc, values


@pytest.mark.parametrize('how', ['relative name', 'relative path', 'relative BOTS_CONFIG_DIR', 'absolute'])
def test_config_directory_may_be_relative(otherenv, how):
    envdir, env = otherenv
    configdir = os.path.join(envdir, 'config')
    if how == 'relative name':
        proc, values = run_init(envdir, env, 'config')
    elif how == 'relative path':
        proc, values = run_init(os.path.dirname(envdir), env, os.path.join(os.path.basename(envdir), 'config'))
    elif how == 'relative BOTS_CONFIG_DIR':
        proc, values = run_init(envdir, dict(env, BOTS_CONFIG_DIR='config'))
    else:
        proc, values = run_init(os.path.dirname(envdir), env, configdir)
    assert proc.returncode == 0, proc.stderr[-800:]
    assert os.path.normcase(values['CONFIG']) == os.path.normcase(configdir)


def test_bots3_ini_spellings_are_accepted(otherenv):
    envdir, env = otherenv
    ini = os.path.join(envdir, 'config', 'bots.ini')
    with open(ini, encoding='utf8') as f:
        txt = f.read()
    start = txt.index('[dirmonitor]')
    end = txt.index('[', start + 5)
    txt = txt[:start] + txt[end:]                                        # no [dirmonitor] section
    txt = txt.replace('log_file_number = 30', 'log_file_number = daily')   # bots 3 way to ask for a daily log
    txt = txt.replace('log_level = INFO', 'log_level = info', 1)
    txt = txt.replace('[webserver]', '[webserver]\nuse_email_address_validation = False', 1)
    assert 'log_file_number = daily' in txt and 'log_level = info' in txt
    with open(ini, 'w', encoding='utf8') as f:
        f.write(txt)
    proc, values = run_init(envdir, env, os.path.join(envdir, 'config'))
    assert proc.returncode == 0, proc.stderr[-800:]
    assert values['LOG_WHEN'] == 'daily'
    assert values['TRIGGER'].endswith('.dirmonitor.trigger')
    assert values['VALIDATE'] == 'False'


def test_settings_of_bots3_are_refused_with_an_explanation(otherenv):
    envdir, env = otherenv
    with open(os.path.join(envdir, 'config', 'settings.py'), 'a', encoding='utf8') as f:
        f.write("\nMIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',)\ndel MIDDLEWARE\n")
    proc, _values = run_init(envdir, env, os.path.join(envdir, 'config'))
    assert proc.returncode != 0
    assert 'is a settings.py of bots 3' in proc.stderr and 'DATABASES' in proc.stderr, proc.stderr[-800:]


def test_relative_usersys_is_the_usersys_of_the_environment(otherenv):
    """'usersys = usersys' (as in a bots.ini of bots 3): not the empty usersys inside the bots package"""
    envdir, env = otherenv
    ini = os.path.join(envdir, 'config', 'bots.ini')
    with open(ini, encoding='utf8') as f:
        lines = f.read().splitlines()
    found = [nr for nr, line in enumerate(lines) if line.split('=')[0].strip() == 'usersys']
    assert len(found) == 1, found
    lines[found[0]] = 'usersys = usersys'
    with open(ini, 'w', encoding='utf8') as f:
        f.write('\n'.join(lines) + '\n')
    # started from another directory, as a service or scheduled task is
    proc, values = run_init(os.path.dirname(envdir), env, os.path.join(envdir, 'config'))
    assert proc.returncode == 0, proc.stderr[-800:]
    assert os.path.normcase(values['USERSYS']) == os.path.normcase(os.path.join(envdir, 'usersys'))


@pytest.mark.parametrize('header, expected', [
    ('plain subject', 'plain subject'),
    ('=?utf-8?q?caf=C3=A9?=', 'caf\xe9'),
    ('RE: =?utf-8?q?caf=C3=A9?= order', 'RE: caf\xe9 order'),              # plain text mixed with an encoded word
    ('=?utf-8?q?a?= =?iso-8859-1?q?b=E9?=', 'ab\xe9'),                      # two encoded words, different charsets
    ('=?iso-8859-1?b?QmVzdGVsbHVuZyBm/HIgS/ZsbiAxMjM0NQ==?=', 'Bestellung f\xfcr K\xf6ln 12345'),
    (None, ''),                                                            # header not in the mail
    ('', ''),
])
def test_mail_header_decoding(header, expected):
    from bots.communication import _comsession
    assert _comsession.checkheaderforcharset(header) == expected


def test_mail_header_with_unknown_charset_is_rejected():
    from bots.communication import _comsession
    from bots.exceptions import CommunicationInError
    with pytest.raises(CommunicationInError):
        _comsession.checkheaderforcharset('=?no-such-charset?q?abc?=')

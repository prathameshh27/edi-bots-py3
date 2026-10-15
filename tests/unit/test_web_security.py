"""Web interface: file names from a request stay inside their directory; database values are escaped."""
import json
import os

import pytest


@pytest.fixture(scope='module')
def web(botsenv):
    """django test client, logged in as superuser; yields (client, environment directory)"""
    from django.conf import settings
    from django.contrib.auth.models import User
    from django.test import Client
    if 'testserver' not in settings.ALLOWED_HOSTS and '*' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']
    user = User.objects.filter(username='ut_admin').first() or User.objects.create_superuser('ut_admin', password='x')
    client = Client()
    client.force_login(user)
    yield client, botsenv, user


def content(response):
    return response.content.decode('utf-8', errors='replace')


def test_path_in_directory(tmp_path):
    from bots import botslib
    base = tmp_path / 'logging'
    (base / 'engine').mkdir(parents=True)
    (tmp_path / 'logging_other').mkdir()
    inside = botslib.path_in_directory(str(base), 'engine', '123')
    assert inside == os.path.realpath(str(base / 'engine' / '123'))
    for name in ('../secret', '..\\secret', '../logging_other/x', str(tmp_path / 'secret'), 'engine/../../secret',
                 '', '.'):
        assert botslib.path_in_directory(str(base), name) is None, name


def test_log_viewer_shows_only_files_of_the_log_directory(web):
    from django.urls import reverse
    client, envdir, _user = web
    logdir = os.path.join(envdir, 'botssys', 'logging', 'engine')
    os.makedirs(logdir, exist_ok=True)
    with open(os.path.join(logdir, '4711'), 'w', encoding='utf8') as f:
        f.write('this is the engine log of run 4711')
    url = reverse('bots:logfiler')
    assert 'this is the engine log of run 4711' in content(client.get(url, {'engine': '4711'}))
    with open(os.path.join(envdir, 'config', 'settings.py'), encoding='utf8') as f:
        assert 'SECRET_KEY' in f.read()
    for name in ('../../../config/settings.py', '..\\..\\..\\config\\settings.py', '../../../config\\settings.py',
                 os.path.join(envdir, 'config', 'settings.py'), '..%2f..%2f..%2fconfig%2fsettings.py'):
        for logname in ('engine', 'webserver', 'jobqueue', 'dirmonitor'):
            assert 'SECRET_KEY' not in content(client.get(url, {logname: name})), (logname, name)
            assert 'SECRET_KEY' not in content(client.get(url, {logname: name, 'action': 'download'})), (logname, name)


def test_source_viewer_shows_only_files_of_usersys(web):
    from django.urls import reverse
    client, envdir, _user = web
    sibling = os.path.join(envdir, 'usersys_other')
    os.makedirs(sibling, exist_ok=True)
    with open(os.path.join(sibling, 'secret.py'), 'w', encoding='utf8') as f:
        f.write('PASSWORD_OF_SOMETHING = 1\n')
    with open(os.path.join(envdir, 'usersys', 'grammars', 'ut_visible.py'), 'w', encoding='utf8') as f:
        f.write('VISIBLE_IN_VIEWER = 1\n')
    url = reverse('bots:srcfiler')
    assert 'VISIBLE_IN_VIEWER' in content(client.get(url, {'src': 'grammars/ut_visible.py'}))
    for name in ('../usersys_other/secret.py', '..\\usersys_other\\secret.py', os.path.join(sibling, 'secret.py'),
                 '../config/settings.py'):
        text = content(client.get(url, {'src': name}))
        assert 'PASSWORD_OF_SOMETHING' not in text and 'SECRET_KEY' not in text, name


def test_saved_selection_is_a_file_of_the_user(web, tmp_path):
    from bots import botsglobal, viewlib
    _client, _envdir, user = web

    class Request:
        GET = {}

    class Form:
        action = '/bots/incoming'

    Request.user = user
    directory = os.path.join(botsglobal.ini.get('directories', 'users'), str(user.id), 'selections', 'incoming')
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, 'mine'), 'w', encoding='utf8') as f:
        json.dump({'idroute': 'x'}, f)
    outside = os.path.join(os.path.dirname(directory), 'outside.json')
    with open(outside, 'w', encoding='utf8') as f:
        json.dump({'secret': 1}, f)
    Request.GET = {'selection': 'mine'}
    assert viewlib.load_selection(Request, Form) == {'idroute': 'x'}
    for name in ('../outside.json', '..\\outside.json', outside, 'sub/../../outside.json'):
        Request.GET = {'selection': name}
        assert viewlib.load_selection(Request, Form) is None, name


def test_admin_lists_escape_values_from_the_database(web):
    from django.urls import reverse
    from bots import models
    client, _envdir, _user = web
    markup = '<img src=x onerror=alert(1)>'
    models.channel(idchannel=markup, inorout='in', type='file', path='x', filename='*').save()
    models.routes(idroute='ut_markup', seq=1, fromchannel_id=markup, fromeditype='<i>edi</i>',
                  frommessagetype='<u>msg</u>', alt='"><b>alt</b>', translateind=1).save()
    try:
        for name in ('admin:bots_channel_changelist', 'admin:bots_routes_changelist'):
            response = client.get(reverse(name))
            text = content(response)
            assert response.status_code == 200, name
            assert '&lt;img src=x onerror=alert(1)&gt;' in text, name
            for raw in (markup, '<i>edi</i>', '<u>msg</u>', '<b>alt</b>'):
                assert raw not in text, (name, raw)
    finally:
        models.routes.objects.filter(idroute='ut_markup').delete()
        models.channel.objects.filter(idchannel=markup).delete()


def test_html_file_is_shown_in_a_sandbox():
    import bots
    template = os.path.join(os.path.dirname(bots.__file__), 'templates', 'bots', 'filer.html')
    with open(template, encoding='utf8') as f:
        text = f.read()
    for line in text.splitlines():
        if 'srcdoc=' in line:
            assert 'sandbox=""' in line
            break
    else:
        pytest.fail('no srcdoc iframe in filer.html')

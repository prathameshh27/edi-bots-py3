"""Web interface: screens and actions that did not work (django test client)."""
import sys

import pytest

EXTERNOUT, FILEOUT, DONE = 520, 500, 3


@pytest.fixture(scope='module')
def client(botsenv):
    from django.conf import settings
    from django.contrib.auth.models import User
    from django.test import Client
    if 'testserver' not in settings.ALLOWED_HOSTS and '*' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']
    user = User.objects.filter(username='ut_webui').first() or User.objects.create_superuser('ut_webui', password='x')
    logged_in = Client()
    logged_in.force_login(user)
    return logged_in


def content(response):
    return response.content.decode('utf-8', errors='replace')


def new_ta(**fields):
    from bots import botslib
    return botslib.NewTransaction(**fields).idta


def test_resend_all_marks_the_files_of_the_selection(client):
    from django.urls import reverse
    from bots import models
    idtas = [new_ta(status=EXTERNOUT, statust=DONE, idroute='ut_r', tochannel='ut_out', filename='utresend%s' % nr)
             for nr in range(3)]
    other = new_ta(status=EXTERNOUT, statust=DONE, idroute='ut_r', tochannel='ut_out', filename='another')
    page = client.get(reverse('bots:outgoing'), {'filename': 'utresend'})
    assert page.status_code == 200 and 'name="resendall"' in content(page)
    # the button posts the form of the screen: the selection is in hidden fields
    import html
    import re
    data = {}
    text = content(page)
    for tag in re.findall(r'<input\b[^>]*>', text):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', tag))
        if not attrs.get('name') or not attrs.get('value') or attrs['name'] == 'csrfmiddlewaretoken':
            continue
        if attrs.get('type') in ('submit', 'button') or (
                attrs.get('type') in ('checkbox', 'radio') and 'checked' not in tag):
            continue
        data[attrs['name']] = html.unescape(attrs['value'])
    for name, options in re.findall(r'<select\b[^>]*\bname="([^"]+)"[^>]*>(.*?)</select>', text, re.S):
        selected = re.findall(r'<option\b[^>]*\bvalue="([^"]*)"[^>]*\bselected', options)
        if selected and selected[0]:
            data[name] = html.unescape(selected[0])
    data['filename'] = 'utresend'
    data['resendall'] = ''
    response = client.post(reverse('bots:outgoing'), data)
    assert response.status_code in (200, 302)
    marked = set(models.ta.objects.filter(retransmit=True).values_list('idta', flat=True))
    assert set(idtas) <= marked and other not in marked


def test_auto_refresh_submits_the_form_of_the_view(client):
    """not the first form of the page: that is the form to log out"""
    from django.urls import reverse
    page = content(client.get(reverse('bots:incoming'), {'refresh': '60'}))
    assert "getElementById('id_refresh').form.submit()" in page
    assert 'document.forms[0].submit()' not in page
    # the first form of the page is indeed the form to log out
    assert 'logout' in page[page.index('<form'):page.index('</form>')]


def test_text_filter_with_two_spaces(client):
    from django.urls import reverse
    for name in ('bots:incoming', 'bots:outgoing'):
        field = 'infilename' if name.endswith('incoming') else 'filename'
        assert client.get(reverse(name), {field: 'a  b'}).status_code == 200


def test_file_viewer_with_a_number_that_is_not_a_number(client):
    from django.urls import reverse
    assert client.get(reverse('bots:filer'), {'idta': 'abc'}).status_code == 404
    assert client.post(reverse('bots:filer'), {'idta': 'abc'}).status_code == 404


def test_manual_confirmations_can_be_selected(botsenv):
    """a manual confirmation is stored as confirmidta -1"""
    from bots import models, viewlib
    manual = new_ta(status=FILEOUT, statust=DONE, idroute='ut_confirm', confirmasked=True, confirmed=True, confirmidta=-1)
    automatic = new_ta(status=FILEOUT, statust=DONE, idroute='ut_confirm', confirmasked=True, confirmed=True,
                       confirmidta=manual)
    found = viewlib.filterquery(
        models.ta.objects.filter(idroute='ut_confirm'), {'confirmidta': -1}, paginate=False)
    found = set(row.idta for row in getattr(found, 'object_list', found))
    assert found == {manual}, (found, manual, automatic)


def test_log_out_on_the_password_pages_is_a_form(client):
    # (django >= 5 does not log out on a link, only on a form that is posted)
    import os
    import bots
    directory = os.path.join(os.path.dirname(bots.__file__), 'templates', 'registration')
    for name in ('password_change_form.html', 'password_change_done.html'):
        with open(os.path.join(directory, name), encoding='utf8') as f:
            text = f.read()
        assert """method="post" action="{% url 'logout' %}\"""" in text, name
        assert """<a href="{% url 'logout' %}\"""" not in text, name


def test_run_engine_does_not_wait_and_uses_this_python(client, monkeypatch):
    from bots import views
    started = []

    class Engine:
        def __init__(self, args, **kwargs):
            started.append(args)

        def wait(self):
            return 0

    monkeypatch.setattr(views.subprocess, 'Popen', Engine)
    # the url as the menu has it, and without anything after 'runengine'
    for url in ('/bots/runengine/?clparameter=--new', '/bots/runengine?clparameter=--new'):
        del started[:]
        response = client.get(url)
        assert response.status_code == 302, url
        assert len(started) == 1, url
        assert started[0][:3] == [sys.executable, '-m', 'bots.engine'] and started[0][-1] == '--new', started
        assert started[0][3].startswith('-c')


def test_about_screen_with_own_title_and_support_link(client):
    from django.urls import reverse
    from bots import bots_context, botsglobal
    url = reverse('bots:home')
    page = content(client.get(url))
    assert 'Bots Open Source EDI Translator' in page and 'Bots documentation' in page

    def about(**settings):
        saved = dict(bots_context.CONTEXT)
        for key, value in settings.items():
            botsglobal.ini.set('webserver', key, value)
        bots_context.CONTEXT.clear()                # read from bots.ini once, at the first request
        try:
            return content(client.get(url))
        finally:
            for key in settings:
                botsglobal.ini.remove_option('webserver', key)
            bots_context.CONTEXT.clear()
            bots_context.CONTEXT.update(saved)

    page = about(about_title='EDI <Monitor>', support_url='https://support.example.com/?a=1&b=2', support_text='Help desk')
    assert '<h1>EDI &lt;Monitor&gt;</h1>' in page and 'Bots Open Source EDI Translator' not in page
    assert 'href="https://support.example.com/?a=1&amp;b=2">Help desk</a>' in page
    assert 'Bots documentation' not in page and 'edi-intelligentsia' not in page
    # only a web or mail address is a link
    page = about(support_url='javascript:alert(1)')
    assert 'javascript:alert' not in page and 'Bots documentation' in page
    assert 'href="mailto:edi@example.com">Support</a>' in about(support_url='mailto:edi@example.com')


def test_context_of_a_request_is_its_own(botsenv):
    from django.contrib.auth.models import User
    from bots import bots_context

    class Request:
        def __init__(self, path, user):
            self.path, self.user = path, user

        def get_full_path(self):
            return self.path

    user = User.objects.filter(is_superuser=True).first()
    first = bots_context.set_context(Request('/bots/incoming/', user))
    second = bots_context.set_context(Request('/bots/outgoing/', user))
    assert first is not second
    assert (first['bots_http_path'], second['bots_http_path']) == ('bots/incoming', 'bots/outgoing')


def test_records_of_bots3_can_be_saved_again(client):
    """found on copies of production databases: a description longer than 256, a database channel without host"""
    from django.contrib import admin
    from django.contrib.auth.models import User
    from bots import models

    def errors(model, **values):
        obj = model(**values)
        request = type('Request', (), {'user': User.objects.filter(is_superuser=True).first(), 'GET': {}, 'POST': {}})()
        form_class = admin.site._registry[model].get_form(request)      # pylint: disable=protected-access
        data = {}
        for name, field in form_class.base_fields.items():
            value = values.get(name, field.initial)
            if value not in (None, False):
                data[name] = 'on' if value is True else value
        return sorted(form_class(data, instance=obj).errors)

    long_text = 'x' * 330
    assert errors(models.translate, fromeditype='x12', frommessagetype='850', tscript='s', toeditype='xml',
                  tomessagetype='order', desc=long_text) == []
    assert errors(models.channel, idchannel='ut_db_nohost', inorout='in', type='db', desc=long_text) == []
    # a channel that connects itself still needs a host
    assert errors(models.channel, idchannel='ut_ftp_nohost', inorout='in', type='ftp') == ['host']


def test_own_logo_and_favicon(client, tmp_path):
    """bots.ini [webserver] logo_image, favicon_image: shown in the page, without changing files of bots"""
    import base64
    from django.urls import reverse
    from bots import bots_context, botsglobal
    png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')
    (tmp_path / 'logo.png').write_bytes(png)
    saved = dict(bots_context.CONTEXT)
    botsglobal.ini.set('webserver', 'logo_image', str(tmp_path / 'logo.png'))
    botsglobal.ini.set('webserver', 'favicon_image', str(tmp_path / 'missing.ico'))
    bots_context.CONTEXT.clear()
    try:
        page = content(client.get(reverse('bots:home')))
    finally:
        botsglobal.ini.remove_option('webserver', 'logo_image')
        botsglobal.ini.remove_option('webserver', 'favicon_image')
        bots_context.CONTEXT.clear()
        bots_context.CONTEXT.update(saved)
    assert 'src="data:image/png;base64,%s"' % base64.b64encode(png).decode() in page
    assert 'img/bots.ico' in page          # favicon file not there: the icon of bots

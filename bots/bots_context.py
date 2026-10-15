"""
Bots context for Django templates rendering

Add it in django settings:

TEMPLATES = [{
    ...
    'OPTIONS': {
        'context_processors':
            'bots.bots_context.set_context'
            ...
"""

import base64
import os

import django
from django.utils import formats

from . import botsglobal
from . import models
from .models import reverse_lazy, _
from . import viewlib


# save vars initialised at startup
CONTEXT = {}


IMAGE_TYPES = {'.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
               '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.webp': 'image/webp'}


def image_data_uri(path):
    """an image file of bots.ini as data uri for an <img> or <link>; '' if not set, not there or too big.
    A relative path is relative to the config directory."""
    if not path:
        return ''
    if not os.path.isabs(path):
        path = os.path.join(botsglobal.ini.get('directories', 'config'), path)
    kind = IMAGE_TYPES.get(os.path.splitext(path)[1].lower())
    try:
        if kind is None or os.path.getsize(path) > 512 * 1024:
            raise OSError('not an image, or too big')
        with open(path, 'rb') as image:
            return 'data:%s;base64,%s' % (kind, base64.b64encode(image.read()).decode('ascii'))
    except OSError:
        botsglobal.logger.warning('Image of bots.ini [webserver] not used: "%s".', path)
        return ''


def set_context(request):
    """set variables in the context of templates."""
    # pylint: disable=too-many-branches
    if not CONTEXT:
        CONTEXT['django_version'] = django.get_version()
        # most context vars are from bots.ini or database. initialise these at startup
        CONTEXT["bots_environment_text"] = (
            botsglobal.ini.get("webserver", "environment_text", None) or ""
        )
        CONTEXT["bots_environment_text_color"] = (
            botsglobal.ini.get("webserver", "environment_text_color", None) or ""
        )
        CONTEXT["bots_environment_text_style"] = (
            botsglobal.ini.get("webserver", "environment_text_style", None) or ""
        )
        if not CONTEXT["bots_environment_text_style"] and CONTEXT["bots_environment_text_color"]:
            CONTEXT["bots_environment_text_style"] = f"color:{CONTEXT['bots_environment_text_color']}"
        CONTEXT['botslogo'] = botsglobal.ini.get('webserver', 'botslogo', 'bots/botslogo.html')
        # own name and support address in the about screen
        CONTEXT['bots_about_title'] = botsglobal.ini.get('webserver', 'about_title', None) or ''
        CONTEXT['bots_support_url'] = botsglobal.ini.get('webserver', 'support_url', None) or ''
        if not CONTEXT['bots_support_url'].lower().startswith(('http://', 'https://', 'mailto:')):
            CONTEXT['bots_support_url'] = ''
        CONTEXT['bots_support_text'] = botsglobal.ini.get('webserver', 'support_text', None) or _('Support')
        # own logo and favicon: image files, shown in the page itself (no change to the files of bots)
        CONTEXT['bots_logo_image'] = image_data_uri(botsglobal.ini.get('webserver', 'logo_image', None))
        CONTEXT['bots_favicon_image'] = image_data_uri(botsglobal.ini.get('webserver', 'favicon_image', None))
        CONTEXT['botsmenu'] = botsglobal.ini.get('webserver', 'botsmenu', 'bots/menu.html')
        CONTEXT["bots_touchscreen"] = botsglobal.ini.getboolean("webserver", "bots_touchscreen", False)
        CONTEXT['menu_automaticretrycommunication'] = botsglobal.ini.getboolean(
            'webserver', 'menu_automaticretrycommunication', False
        )
        CONTEXT["menu_cleanup"] = botsglobal.ini.getboolean("webserver", "menu_cleanup", False)
        CONTEXT["menu_changepassword"] = botsglobal.ini.getboolean("webserver", "menu_changepassword", True)
        # in bots.ini it is possible to add custom menus
        if botsglobal.ini.has_section('custommenus'):
            CONTEXT['custom_menuname'] = botsglobal.ini.get('custommenus', 'menuname', 'Custom')
            CONTEXT['custom_menus'] = [
                (key.title(), value)
                for key, value in botsglobal.ini.items('custommenus')
                if key != 'menuname'
            ]
        CONTEXT['editypes'] = models.EDITYPES
        CONTEXT['channeltypes'] = models.CHANNELTYPE

        # Date/Time input formats 'Y-m-d H:i:s'
        # Format used for javascript and templates without '%' (not python datetime format)
        for key in ['DATETIME_INPUT_FORMAT', 'DATE_INPUT_FORMAT', 'TIME_INPUT_FORMAT']:
            # (DATE/TIME)_INPUT_FORMATS
            idx = -1 if key.startswith('TIME') else 0
            CONTEXT[key] = formats.get_format_lazy(f"{key}S")[idx].replace(
                '%', '').replace('M', 'i').replace('S', 's')

    # what follows is per request: in a context of its own (requests are handled at the same time)
    context = dict(CONTEXT)
    return request_context(request, context)


def request_context(request, CONTEXT):
    """add the variables that depend on the request, the user or the database."""
    # pylint: disable=invalid-name
    # in bots.ini can be indicated that all routes (in config->routes, if route is activated)
    # can be run individually via menu
    if botsglobal.ini.get('webserver', 'menu_all_routes', '') == 'notindefaultrun':
        CONTEXT['menu_all_routes'] = list(
            models.routes.objects.values_list('idroute', flat=True)
            .filter(active=True)
            .filter(notindefaultrun=True)
            .order_by('idroute')
            .distinct()
        )
    elif botsglobal.ini.getboolean('webserver', 'menu_all_routes', False):
        CONTEXT['menu_all_routes'] = list(
            models.routes.objects.values_list('idroute', flat=True)
            .filter(active=True)
            .order_by('idroute')
            .distinct()
        )

    # bots_http_path is used in name of browser-window; this is derived from url/path
    bots_http_path = request.get_full_path()
    if bots_http_path.startswith(str(reverse_lazy('admin:app_list', kwargs={'app_label': 'bots'}))):
        bots_http_path = bots_http_path[12:]
    else:
        bots_http_path = bots_http_path[1:]
    if bots_http_path:
        if bots_http_path[-1] == '/':
            bots_http_path = bots_http_path[:-1]
    else:
        bots_http_path = 'home'
    CONTEXT['bots_http_path'] = bots_http_path

    # mindate/maxdate
    CONTEXT['bots_mindate'] = viewlib.datetimefrom()
    CONTEXT['bots_maxdate'] = viewlib.datetimeuntil()

    # Shortcuts
    CONTEXT['shortcuts_menuname'] = ''
    shortcuttrigger = models.ccodetrigger.objects.filter(ccodeid='shortcut').first()
    if shortcuttrigger:
        CONTEXT['shortcuts'] = shortcuts = {}
        # Append global and user shortcuts
        for shortcut in models.ccode.objects.filter(
                ccodeid='shortcut', attr8__in=['', str(request.user.id)],
                ).exclude(leftcode='menuname').order_by('attr2', 'leftcode'):
            shortcuts.setdefault(shortcut.attr2, [])
            shortcuts[shortcut.attr2].append(
                (shortcut.leftcode.title(), shortcut.rightcode + shortcut.attr1))

        # shortcuts_menuname
        CONTEXT['shortcuts_menuname'] = _('Shortcuts')
        shortcuts_menuname = models.ccode.objects.filter(
            ccodeid='shortcut', leftcode='menuname').first()
        if shortcuts_menuname:
            CONTEXT['shortcuts_menuname'] = shortcuts_menuname.rightcode

    # ***variables are set now for template use, eg {{ bots_environment_text }}
    return CONTEXT

# -*- coding: utf-8 -*-
"""
bots-portconfig: carry the configuration of a bots 3 installation over to an environment of this bots.

    bots-portconfig <config directory of bots 3> <config directory of the new environment> [--write]

Without --write nothing is changed: it only lists what would be done.

 - bots.ini: every option of the bots.ini of bots 3 gets its value in the new bots.ini, when this bots knows the
   option. Not: the directories, and the sample directory monitors of the bots 3 distribution.
   The new bots.ini keeps its comments; a changed line is marked.
 - settings.py: the mail settings for error reports (MANAGERS, EMAIL_HOST...), time zone, session settings and
   secret key are added at the end of the new settings.py, in the form this bots uses.
   The database is not carried over: it is reported if bots 3 did not use the default SQLite database.

The files of bots 3 are only read. A bots.ini of bots 3 may have a section or option twice (the last counts).
"""
import ast
import configparser
import datetime
import os
import re
import sys

# options of bots 3 that this bots reads under another name: (section, option): (section, option)
RENAMED = {
    ('webserver', 'use_email_address_validation'): ('webserver', 'validate_email_address'),
}
# options of bots 3 that have no function in this bots: (section, option): why
DROPPED = {
    ('jobqueue', 'lauchfrequency'): 'the job queue starts a job at once; it does not look every n seconds',
    ('dirmonitor', 'lauchfrequency'): 'the directory monitor hands a job over at once',
    ('settings', 'compatibility_handle_message_errors'): 'was for mappings of before bots 3.0',
}
NOT_CARRIED = {
    ('directories', 'botssys'), ('directories', 'usersys'), ('directories', 'config'),
    ('directories', 'botspath'), ('directories', 'data'), ('directories', 'logging'),
    ('directories', 'templatehtml'), ('directories', 'usersysabs'),
}
# the directory monitors in the bots.ini of the bots 3 distribution are examples
SAMPLE_PATH = re.compile(r'/hje/.*/infile/stress06/')
# settings.py of bots 3: what is carried over, with the default of bots 3.2.0 (a default is not carried)
SETTINGS = {
    'MANAGERS': (('name_manager', 'adress@test.com'),),
    'EMAIL_HOST': 'localhost', 'EMAIL_PORT': '25', 'EMAIL_USE_TLS': False, 'EMAIL_USE_SSL': False,
    'EMAIL_HOST_USER': '', 'EMAIL_HOST_PASSWORD': '', 'SERVER_EMAIL': None, 'EMAIL_SUBJECT_PREFIX': None,
    'TIME_ZONE': None, 'LANGUAGE_CODE': None,        # always carried: the default of this bots is another
    'SESSION_EXPIRE_AT_BROWSER_CLOSE': True, 'SESSION_COOKIE_AGE': 3600, 'SESSION_SAVE_EVERY_REQUEST': True,
    'SECRET_KEY': 'm@-u37qiujmeqfbu$daaaaz)sp^7an4u@h=wfx9dd$$$zl2i*x9#awojdc',
}
MAILER = {'EMAIL_HOST': 'host', 'EMAIL_PORT': 'port', 'EMAIL_USE_TLS': 'use_tls', 'EMAIL_USE_SSL': 'use_ssl',
          'EMAIL_HOST_USER': 'username', 'EMAIL_HOST_PASSWORD': 'password'}
SECRET = ('EMAIL_HOST_PASSWORD', 'SECRET_KEY')
MARK_START = '# ----- carried over from bots 3 by bots-portconfig'
MARK_END = '# ----- end of what bots-portconfig carried over'


def read_ini(path):
    """bots.ini as python 2 read it: a section or option twice is not an error"""
    ini = configparser.RawConfigParser(strict=False)
    with open(path, 'rb') as f:
        data = f.read()
    try:
        ini.read_string(data.decode('utf-8'))
    except UnicodeDecodeError:
        ini.read_string(data.decode('latin-1'))
    return ini


def known_options(new_text):
    """{section: {option: 'active' or 'commented'}} of the new bots.ini; a commented option is one this bots knows"""
    known, section = {}, None
    for line in new_text.splitlines():
        header = re.match(r'^\[([^\]]+)\]\s*$', line)
        if header:
            section = header.group(1)
            known.setdefault(section, {})
            continue
        if section is None:
            continue
        active = re.match(r'^([A-Za-z_][\w.-]*)\s*[=:]', line)
        if active:
            known[section][active.group(1).lower()] = 'active'
            continue
        commented = re.match(r'^#\s?([a-z_][a-z0-9_]*)\s*=', line)
        if commented:
            known[section].setdefault(commented.group(1).lower(), 'commented')
    return known


def plan_ini(old, new_text):
    """what to do with the options of the bots.ini of bots 3.
    Returns (changes [(section, option, new value, value now or None)], notes [(section, option, why)])"""
    new = configparser.RawConfigParser(strict=False)
    new.read_string(new_text)
    known = known_options(new_text)
    changes, notes = [], []
    for section in old.sections():
        for option, value in old.items(section):
            target = RENAMED.get((section, option), (section, option))
            if (section, option) in NOT_CARRIED:
                continue
            if (section, option) in DROPPED:
                notes.append((section, option, 'not used any more: ' + DROPPED[(section, option)]))
                continue
            if section.startswith('dirmonitor') and section != 'dirmonitor' and SAMPLE_PATH.search(
                    old.get(section, 'path') if old.has_option(section, 'path') else ''):
                continue
            free_section = section in ('custommenus', 'charsets') or (
                section.startswith('dirmonitor') and section != 'dirmonitor')
            if not free_section and target[1] not in known.get(target[0], {}):
                notes.append((section, option, 'not known to this bots: not carried over'))
                continue
            now = new.get(*target) if new.has_option(*target) else None
            if now != value:
                changes.append((target[0], target[1], value, now))
            if target != (section, option):
                notes.append((section, option, 'is now [%s] %s' % target))
    return changes, notes


def apply_ini(new_text, changes):
    """the new bots.ini with the changes; comments and order are kept"""
    newline = '\r\n' if '\r\n' in new_text else '\n'
    lines = new_text.splitlines()
    for section, option, value, _now in changes:
        start = end = None
        for number, line in enumerate(lines):
            header = re.match(r'^\[([^\]]+)\]\s*$', line)
            if header:
                if start is not None:
                    end = number
                    break
                if header.group(1) == section:
                    start = number
        if start is None:
            lines += ['', '[%s]' % section]
            start = len(lines) - 1
        end = len(lines) if end is None else end
        setting = '%s = %s' % (option, value)
        active = [n for n in range(start + 1, end) if re.match(r'^%s\s*[=:]' % re.escape(option), lines[n], re.I)]
        commented = [n for n in range(start + 1, end) if re.match(r'^#\s?%s\s*=' % re.escape(option), lines[n])]
        if active:
            lines[active[-1]] = setting
            for number in reversed(active[:-1]):
                del lines[number]
        elif commented:
            lines.insert(commented[-1] + 1, setting)
        else:
            lines.insert(start + 1, setting)
    return newline.join(lines) + newline


def read_settings(path):
    """the simple assignments in the settings.py of bots 3 (it is not run): {name: value}; and the database engine"""
    with open(path, 'rb') as f:
        data = f.read()
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        text = data.decode('latin-1')
    found, engine = {}, None
    try:
        tree = ast.parse(text)
    except SyntaxError:
        # python 2 only syntax somewhere: take the assignments line by line
        tree = ast.Module(body=[], type_ignores=[])
        for line in text.splitlines():
            if re.match(r'^[A-Z_][A-Z0-9_]*\s*=', line):
                try:
                    tree.body += ast.parse(line).body
                except SyntaxError:
                    pass
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            try:
                found[name] = ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                if name == 'DATABASES':
                    engines = re.findall(r"""['"]ENGINE['"]\s*:\s*['"]([^'"]+)['"]""", ast.get_source_segment(text, node) or '')
                    engine = engines[0] if engines else None
    if 'DATABASES' in found:
        engine = (found['DATABASES'].get('default') or {}).get('ENGINE')
    return found, engine


def plan_settings(found):
    """python lines for the end of the new settings.py, and what is carried (names)"""
    carried = [name for name in SETTINGS if name in found and found[name] != SETTINGS[name]]
    lines = []
    mailer = dict((MAILER[name], found[name]) for name in carried if name in MAILER)
    if 'port' in mailer:
        try:
            mailer['port'] = int(mailer['port'])
        except (TypeError, ValueError):
            pass
    if mailer:
        lines.append("MAILERS['default']['OPTIONS'].update(%r)" % (mailer,))
    for name in carried:
        if name not in MAILER:
            lines.append('%s = %r' % (name, found[name]))
    return lines, carried


def apply_settings(new_text, lines):
    newline = '\r\n' if '\r\n' in new_text else '\n'
    text = re.sub(r'(?s)\r?\n?%s.*?%s[^\n]*\r?\n?' % (re.escape(MARK_START), re.escape(MARK_END)), newline, new_text)
    if not lines:
        return text
    block = ['', '%s (%s)' % (MARK_START, datetime.date.today().isoformat())] + lines + [MARK_END, '']
    return text.rstrip('\r\n') + newline + newline.join(block)


def port(old_dir, new_dir, write=False, out=print):
    """Returns True if all could be read. Changes the new bots.ini and settings.py only if write is True."""
    ok = True
    old_ini, new_ini = os.path.join(old_dir, 'bots.ini'), os.path.join(new_dir, 'bots.ini')
    for path in (old_ini, new_ini):
        if not os.path.isfile(path):
            out('Not found: %s' % path)
            return False
    with open(new_ini, 'rb') as f:
        new_text = f.read().decode('utf-8')
    changes, notes = plan_ini(read_ini(old_ini), new_text)
    out('bots.ini: %d setting(s) %s' % (len(changes), 'changed' if write else 'to change'))
    for section, option, value, now in changes:
        out('    [%s] %s = %s%s' % (section, option, value, '' if now is None else '   (was: %s)' % now))
    for section, option, why in notes:
        out('    [%s] %s: %s' % (section, option, why))
    if write and changes:
        with open(new_ini, 'wb') as f:
            f.write(apply_ini(new_text, changes).encode('utf-8'))

    old_settings, new_settings = os.path.join(old_dir, 'settings.py'), os.path.join(new_dir, 'settings.py')
    if not os.path.isfile(old_settings):
        out('settings.py: no settings.py of bots 3 in %s' % old_dir)
        return ok
    if not os.path.isfile(new_settings):
        out('Not found: %s' % new_settings)
        return False
    found, engine = read_settings(old_settings)
    lines, carried = plan_settings(found)
    out('settings.py: %d setting(s) %s' % (len(carried), 'carried over' if write else 'to carry over'))
    for name in carried:
        out('    %s%s' % (name, '' if name in SECRET else ' = %r' % (found[name],)))
    if engine and 'sqlite' not in engine:
        out('    DATABASES: bots 3 used "%s". Not carried over: set the database in the new settings.py by hand'
            % engine)
    if write:
        with open(new_settings, 'rb') as f:
            text = f.read().decode('utf-8')
        with open(new_settings, 'wb') as f:
            f.write(apply_settings(text, lines).encode('utf-8'))
    if not write:
        out('Nothing is changed. Use --write to change %s' % new_dir)
    return ok


def start():
    arguments = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    options = [arg for arg in sys.argv[1:] if arg.startswith('-')]
    if len(arguments) != 2 or [arg for arg in options if arg != '--write']:
        print(__doc__)
        sys.exit(1)
    sys.exit(0 if port(arguments[0], arguments[1], write='--write' in options) else 1)


if __name__ == '__main__':
    start()

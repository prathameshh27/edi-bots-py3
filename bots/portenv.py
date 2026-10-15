# -*- coding: utf-8 -*-
"""
bots-portenv: make an environment of this bots from an environment of bots 3 (python 2).

    bots-portenv --bots3=<directory of bots 3> [--number=<N>] <new environment directory>
    bots-portenv --usersys=<dir> --config=<dir> --database=<file> <new environment directory>

    --bots3=<dir>      directory with the program of bots 3 (it has config, usersys and botssys in it).
    --number=<N>       for an installation with more environments next to each other: config<N>, usersys<N>,
                       botssys<N>. Without it: config, usersys, botssys.
    --usersys, --config, --database   give the three places yourself (database: the SQLite file).
    --no-database      do not copy and upgrade a database (bots 3 used MySQL or PostgreSQL: see the guide).
    --bots3-dir-on-server=<dir>
                       the directory of the bots 3 program on the server where it runs (eg /home/edi/bots).
                       A file channel with a relative path (relative to that directory in bots 3) gets the full
                       path, so that it uses the same folder as before. Without it relative paths are listed.
    --local-folders    for a test environment (eg on another machine than bots 3): every folder of a file channel
                       is made inside the new environment (<env>/channels/<path as it was>); every other channel
                       (ftp, sftp, mail, database...) gets a testpath there, and bots.ini gets
                       channels_use_testpath = True: nothing is sent to or fetched from another machine.
    --processes=<n>    check usersys with n processes (default 1).

Does, in this order:
  1. makes the new environment directory (it must not exist, or be empty): config, botssys, usersys
  2. usersys: copies it converted to python 3 (bots-portusersys); lines to look at -> port-review.txt
  3. database: copies the SQLite file of bots 3 and upgrades the copy (bots-updatedb)
  4. configuration: carries bots.ini and settings.py over (bots-portconfig)
  5. checks every grammar and script of the new usersys (bots-checkusersys) -> port-check.json

Nothing of bots 3 is changed: all is read or copied. Bots 3 should not be running while its database is copied.
The data files of bots 3 (botssys/data) are not copied: see the migration guide.
Exit code: 0 all steps done and no errors found; 1 done, with things to look at; 2 not done.
"""
import ntpath
import os
import posixpath
import shutil
import sqlite3
import subprocess
import sys


def run(code, args, configdir=None):
    """a step in a process of its own (bots can be initialised once per process)"""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for key in ('BOTS_CONFIG_DIR', 'BOTSENV', 'DJANGO_SETTINGS_MODULE'):
        env.pop(key, None)
    if configdir:
        env['BOTS_CONFIG_DIR'] = configdir
    proc = subprocess.run([sys.executable, '-c', code] + list(args), env=env, capture_output=True, text=True,
                          errors='replace', check=False)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def tail(text, lines=12):
    return '\n'.join('      ' + line for line in text.splitlines()[-lines:])


def absolute_channel_paths(database, directory):
    """File channels with a relative path get the full path: directory + relative path (as bots 3 used it).
    Returns [(idchannel, field, old path, new path)]."""
    join = posixpath.join if directory.startswith('/') else ntpath.join
    changed = []
    connection = sqlite3.connect(database)
    try:
        for idchannel, path, testpath, archivepath in connection.execute(
                "SELECT idchannel, path, testpath, archivepath FROM channel WHERE type IN ('file', 'mimefile', 'trash') "
                "ORDER BY idchannel").fetchall():
            for field, value in (('path', path), ('testpath', testpath), ('archivepath', archivepath)):
                if value and not posixpath.isabs(value) and not ntpath.isabs(value):
                    new = join(directory, value)
                    connection.execute('UPDATE channel SET %s=? WHERE idchannel=?' % field, (new, idchannel))
                    changed.append((idchannel, field, value, new))
        connection.commit()
    finally:
        connection.close()
    return changed


FILE_TYPES = ('file', 'mimefile', 'trash')


def local_folder(envdir, path):
    """<envdir>/channels/<path>: a path of bots 3 (relative, /home/..., C:/...) as a folder inside the environment"""
    parts = [part for part in path.replace('\\', '/').split('/') if part and part not in ('.', '..')]
    if parts and parts[0].endswith(':'):
        parts[0] = parts[0][:-1]
    return os.path.join(envdir, 'channels', *parts)


def local_folders(database, envdir):
    """All channels on this machine (see --local-folders). Returns [(idchannel, field, old, new)]."""
    changed = []
    connection = sqlite3.connect(database)
    try:
        for idchannel, inorout, kind, path, testpath, archivepath in connection.execute(
                'SELECT idchannel, inorout, type, path, testpath, archivepath FROM channel ORDER BY idchannel').fetchall():
            values = {}
            if kind in FILE_TYPES:
                for field, value in (('path', path), ('archivepath', archivepath), ('testpath', testpath)):
                    if value:
                        values[field] = local_folder(envdir, value)
            else:
                values['testpath'] = os.path.join(envdir, 'channels', 'test', inorout or 'x', idchannel)
            for field, new in values.items():
                os.makedirs(new, exist_ok=True)
                connection.execute('UPDATE channel SET %s=? WHERE idchannel=?' % field, (new, idchannel))
                changed.append((idchannel, field, {'path': path, 'archivepath': archivepath, 'testpath': testpath}[field], new))
        connection.commit()
    finally:
        connection.close()
    return changed


def set_channels_use_testpath(configdir):
    ini = os.path.join(configdir, 'bots.ini')
    with open(ini, encoding='utf8') as f:
        text = f.read()
    lines = text.splitlines()
    lines = [line for line in lines if not line.strip().startswith('channels_use_testpath')]
    index = next(number for number, line in enumerate(lines) if line.strip() == '[settings]')
    lines.insert(index + 1, 'channels_use_testpath = True')
    with open(ini, 'w', encoding='utf8') as f:
        f.write('\n'.join(lines) + '\n')


def port_environment(usersys, config, database, target, processes=1, out=print, bots3_dir_on_server=None,
                     local=False):
    """Returns the exit code (see the module text)."""
    # pylint: disable=too-many-return-statements, too-many-branches, too-many-statements
    for label, path, isdir in (('usersys', usersys, True), ('config', config, True), ('database', database, False)):
        if path is None:
            continue
        if not (os.path.isdir(path) if isdir else os.path.isfile(path)):
            out('Not found: %s of bots 3: %s' % (label, path))
            return 2
    if database:
        with open(database, 'rb') as f:
            if f.read(16) != b'SQLite format 3\x00':
                out('The database "%s" is not a SQLite file. Use --no-database and see the migration guide.' % database)
                return 2
    target = os.path.abspath(target)
    if os.path.exists(target) and os.listdir(target):
        out('The new environment directory exists and is not empty: %s' % target)
        return 2
    attention = False

    out('1. new environment: %s' % target)
    code, text = run('import sys; from bots import botsinit; '
                     'sys.exit(0 if botsinit.initbotsenv(botsenv_path=sys.argv[1], interactive=False) else 1)', [target])
    configdir = os.path.join(target, 'config')
    if code or not os.path.isfile(os.path.join(configdir, 'bots.ini')):
        out('   could not be made:\n%s' % tail(text))
        return 2

    out('2. usersys: %s' % usersys)
    from . import portusersys
    tool = portusersys.refactoringtool()
    new_usersys = os.path.join(target, 'usersys')
    shutil.rmtree(new_usersys)
    report = portusersys.port_tree(usersys, new_usersys, tool=tool)
    for dirpath, _dirs, files in os.walk(new_usersys):
        if '__init__.py' not in files:
            with open(os.path.join(dirpath, '__init__.py'), 'w', encoding='utf8'):
                pass
    review = os.path.join(target, 'port-review.txt')
    portusersys.write_review(report, review)
    lines = sum(len(found) for found in report.review.values())
    out('   %d files, %d python; %d changed; %d could not be converted; %d lines to look at%s' % (
        report.files, report.python, len(report.changed), len(report.errors), lines,
        ' (%s)' % review if lines else ''))
    if tool is None and report.errors:
        out('   python library "fissix" is not installed: files that are python 2 only are not converted')
    for name, error in sorted(report.errors.items())[:20]:
        out('      %s: %s' % (name, str(error)[:150]))
    attention = attention or bool(report.errors) or bool(lines)

    if database:
        out('3. database: %s' % database)
        shutil.copyfile(database, os.path.join(target, 'botssys', 'sqlitedb', 'botsdb'))
        code, text = run("import sys; sys.argv[0] = 'bots-updatedb'; from bots.botsupdatedb import start; start()",
                         ['--yes-i-have-a-backup'], configdir)       # the backup: the database of bots 3 itself
        out(tail(text, 6))
        if code:
            out('   the copy of the database could not be upgraded (exit code %s)' % code)
            return 2
        if bots3_dir_on_server:
            changed = absolute_channel_paths(os.path.join(target, 'botssys', 'sqlitedb', 'botsdb'), bots3_dir_on_server)
            out('   file channels with a relative path: %d path(s) made full, relative to %s' % (
                len(changed), bots3_dir_on_server))
            for idchannel, field, old, new in changed:
                out('      channel %s %s: %s -> %s' % (idchannel, field, old, new))
    else:
        out('3. database: not copied (--no-database). The new environment has an empty database.')
        attention = True

    out('4. configuration: %s' % config)
    from . import portconfig
    if not portconfig.port(config, configdir, write=True, out=lambda line: out('   ' + line)):
        attention = True

    if local and database:
        changed = local_folders(os.path.join(target, 'botssys', 'sqlitedb', 'botsdb'), target)
        set_channels_use_testpath(configdir)
        out('   local folders: %d channel folder(s) inside %s; bots.ini: channels_use_testpath = True' % (
            len(changed), os.path.join(target, 'channels')))
    out('5. check of the new usersys')
    result = os.path.join(target, 'port-check.json')
    code, text = run("import sys; sys.argv[0] = 'bots-checkusersys'; from bots.portusersys import start_check; "
                     "start_check()", ['--processes=%d' % processes, '--json=' + result], configdir)
    out(tail(text, 40))
    attention = attention or bool(code)

    out('')
    out('Done: %s' % target)
    out('Use it with: -c%s   (or environment variable BOTS_CONFIG_DIR)' % configdir)
    out('Still to do by hand: the items above marked as error or "to look at"; paths of file channels and the')
    out('data files of bots 3 (see the migration guide); a first run with the channels switched to test.')
    return 1 if attention else 0


def start():
    options, arguments = {}, []
    for arg in sys.argv[1:]:
        if arg.startswith('--'):
            key, _sep, value = arg[2:].partition('=')
            options[key] = value
        else:
            arguments.append(arg)
    known = {'bots3', 'number', 'usersys', 'config', 'database', 'no-database', 'processes', 'bots3-dir-on-server',
             'local-folders'}
    if len(arguments) != 1 or set(options) - known or not (
            'bots3' in options or {'usersys', 'config'} <= set(options)):
        print(__doc__)
        sys.exit(2)
    usersys, config, database = options.get('usersys'), options.get('config'), options.get('database')
    if 'bots3' in options:
        number = options.get('number', '')
        usersys = usersys or os.path.join(options['bots3'], 'usersys' + number)
        config = config or os.path.join(options['bots3'], 'config' + number)
        database = database or os.path.join(options['bots3'], 'botssys' + number, 'sqlitedb', 'botsdb')
    if 'no-database' in options:
        database = None
    elif not database:
        print('Give --database=<SQLite file of bots 3>, or --no-database.')
        sys.exit(2)
    sys.exit(port_environment(usersys, config, database, arguments[0], int(options.get('processes') or 1),
                              bots3_dir_on_server=options.get('bots3-dir-on-server'),
                              local='local-folders' in options))


if __name__ == '__main__':
    start()

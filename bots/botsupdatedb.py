"""
bots-updatedb: bring the bots database to this version of bots.

- empty database: all tables are created;
- database of bots 3 (3.0 - 3.2): upgraded in place (make a backup first!);
- database of an earlier bots 4: pending changes are applied;
- anything else (bots 2 or older, not a bots database): refused.
"""
import os
import sys

# bots-modules
from . import botsglobal
from . import botsinit
from . import botslib
from . import dbschema

EMPTY, BOTS3, BOTS4, UNKNOWN = 'empty', 'bots3', 'bots4', 'unknown'
STATETEXT = {
    EMPTY: 'empty (no bots tables)',
    BOTS3: 'made by bots 3',
    BOTS4: 'made by bots 4',
    UNKNOWN: 'not recognised',
}
# tables django manages for bots / columns that are in a bots 3 database but not in a bots 2 database
MANAGED_TABLES = ('routes', 'channel', 'partner', 'translate', 'chanpar', 'ccode', 'ccodetrigger',
                  'confirmrule', 'filereport', 'report')
BOTS3_COLUMNS = {'routes': ('zip_incoming', 'zip_outgoing'), 'channel': ('testpath', 'keyfile'),
                 'report': ('acceptance', 'filesize')}
# screens every user that was logged in could see in bots 3; in bots 4 these need a permission
VIEW_FOR_ALL = ('view_report', 'view_filereport', 'view_ta')
FILE_CHANNELS = ('file', 'mimefile', 'trash')

USAGE = """
    This is "%(name)s" version %(version)s, part of Bots open source edi translator (https://bots-edi.org).
    Brings the bots database to version %(version)s: a new (empty) database, or the database of bots 3.

    Usage:
        %(name)s [options]
    Options:
        -c<directory>           directory for configuration files (default: config).
        --check                 only report: what is the database, what would be done. Changes nothing.
        --yes-i-have-a-backup   needed to upgrade the database of bots 3: that can not be undone.
        --createsuperuser       after the update: create a user that can log in (asks name and password).

    Exit code: 0 OK (with --check: nothing to do); 1 with --check: there is something to do;
               2 database not recognised, or not confirmed there is a backup; 3 other errors.
"""


def columns(connection, table):
    with connection.cursor() as cursor:
        return set(col.name for col in connection.introspection.get_table_description(cursor, table))


def database_state(connection):
    """Returns (state, explanation)."""
    tables = set(connection.introspection.table_names())
    present = [table for table in MANAGED_TABLES + dbschema.ENGINE_TABLES if table in tables]
    if not present:
        return EMPTY, ''
    missing = [table for table in MANAGED_TABLES if table not in tables]
    if missing:
        return UNKNOWN, 'tables %s exist, but not %s' % (', '.join(present), ', '.join(missing))
    if 'django_migrations' in tables:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app = 'bots'")
            if cursor.fetchone()[0]:
                return BOTS4, ''
    for table, names in BOTS3_COLUMNS.items():
        notfound = [name for name in names if name not in columns(connection, table)]
        if notfound:
            return UNKNOWN, 'table %s has no column %s: older than bots 3? Use bots 3 to update to bots 3 first.' % (
                table, ', '.join(notfound))
    missing = [table for table in dbschema.ENGINE_TABLES if table not in tables]
    if missing:
        return UNKNOWN, 'bots 3 database without table(s) %s' % ', '.join(missing)
    return BOTS3, ''


def pending_migrations(connection):
    from django.db.migrations.executor import MigrationExecutor
    executor = MigrationExecutor(connection)
    return ['%s.%s' % (migration.app_label, migration.name)
            for migration, _backwards in executor.migration_plan(executor.loader.graph.leaf_nodes())]


def relative_channel_paths():
    """
    File channels with a relative path. Such a path is relative to the bots directory ('botspath');
    after installing a new bots that directory is another one.
    Returns list of (idchannel, path, absolute path)
    """
    from . import models
    found = []
    for channel in models.channel.objects.filter(type__in=FILE_CHANNELS).order_by('idchannel'):
        for path in sorted(set((channel.path, channel.testpath))):
            if path and not os.path.isabs(path):
                found.append((channel.idchannel, path, botslib.join(path)))
    return found


TLS_CHANNELS = ('pop3s', 'imap4s', 'smtps', 'smtpstarttls', 'ftps', 'ftpis', 'https')


def keep_tls_as_in_bots3():
    """
    Bots 3 did not verify the certificate of a server. The channels of a bots 3 database keep connecting
    as they did: 'verify_cert' is set off for the channels that exist. New channels verify.
    Returns list of the idchannel of channels with TLS.
    """
    from . import models
    models.channel.objects.update(verify_cert=False)
    return list(models.channel.objects.filter(type__in=TLS_CHANNELS).order_by('idchannel').values_list(
        'idchannel', flat=True))


def grant_view_permissions():
    """
    Bots 4 (django >= 2.1) has a permission 'view'. Give it to who could see the same in bots 3:
    - users and groups that can change X can view X;
    - active users can view reports, incoming files and transactions.
    Returns number of permissions given.
    """
    from django.contrib.auth.models import Group, Permission, User
    perms = dict((perm.codename, perm) for perm in Permission.objects.filter(content_type__app_label='bots'))
    count = 0
    holders = [(user, user.user_permissions) for user in User.objects.filter(is_superuser=False)]
    holders += [(group, group.permissions) for group in Group.objects.all()]
    for holder, related in holders:
        has = set(related.filter(content_type__app_label='bots').values_list('codename', flat=True))
        wanted = set('view_' + codename[len('change_'):] for codename in has if codename.startswith('change_'))
        if isinstance(holder, User) and holder.is_active:
            wanted.update(VIEW_FOR_ALL)
        for codename in sorted(wanted - has):
            if codename in perms:
                related.add(perms[codename])
                count += 1
    return count


def update(check=False, backup_confirmed=False, out=print):
    """Do the update (or with check: report what is to do). Returns exit code."""
    # pylint: disable=too-many-branches, too-many-return-statements
    from django.core.management import call_command
    from django.db import connection

    out('Database: %s "%s".' % (connection.vendor, connection.settings_dict['NAME']))
    state, why = database_state(connection)
    out('This database is: %s%s.' % (STATETEXT[state], ' (%s)' % why if why else ''))
    if state == UNKNOWN:
        out('Nothing is changed.')
        return 2

    pending = pending_migrations(connection)
    narrow = dbschema.narrow_columns(connection) if state != EMPTY else []
    if check:
        if state == BOTS4 and not pending and not narrow:
            out('The database is up to date.')
            return 0
        out('To do: %s.' % {EMPTY: 'create the tables', BOTS3: 'upgrade to bots 4', BOTS4: 'apply changes'}[state])
        out('    %s changes (migrations) of the tables of django and bots' % len(pending))
        for table, name, current, length in narrow:
            out('    widen %s.%s: %s -> %s' % (table, name, current, length))
        if state == BOTS3:
            out('    give users the new permission "view"')
            out('Make a backup of the database and run again with --yes-i-have-a-backup.')
        return 1

    if state == BOTS3 and not backup_confirmed:
        out('Upgrading a bots 3 database can not be undone, and bots 3 can not use the database afterwards.\n'
            'Make a backup of the database and run again with --yes-i-have-a-backup.\n'
            'Nothing is changed.')
        return 2

    if state == BOTS3:
        # the tables of bots 3 are what the first migrations would make: register these as done
        call_command('migrate', fake_initial=True, interactive=False, verbosity=1)
    else:
        call_command('migrate', interactive=False, verbosity=1)
    # also done in the migrations; here for a database that had these migrations before the tables
    for text in dbschema.ensure_engine_tables(connection):
        out(text)
    if state == BOTS3:
        out('Permissions "view" given: %s.' % grant_view_permissions())
        notverified = keep_tls_as_in_bots3()
        if notverified:
            out('Channels with TLS/SSL: the certificate of the server is not verified, as in bots 3.\n'
                'Advised: tick "Verify server certificate" in the channel (and set "CA certificate file" if needed):')
            out('    ' + ', '.join(notverified))
        relative = relative_channel_paths()
        if relative:
            out('Channels with a relative path; check if this is the directory you expect:')
            for idchannel, path, absolute in relative:
                out('    channel %s: "%s" is "%s"' % (idchannel, path, absolute))
    out('The database is up to date.')
    return 0


def start():
    usage = USAGE % {'name': os.path.basename(sys.argv[0]), 'version': botsglobal.version}
    configdir = None
    check = backup_confirmed = createsuperuser = False
    for arg in sys.argv[1:]:
        if arg.startswith('-c') and not arg.startswith('--'):
            configdir = arg[2:]
            if not configdir:
                print('Error: configuration directory indicated, but no directory name.')
                sys.exit(3)
        elif arg == '--check':
            check = True
        elif arg == '--yes-i-have-a-backup':
            backup_confirmed = True
        elif arg == '--createsuperuser':
            createsuperuser = True
        else:
            print(usage)
            sys.exit(0)
    # find locating of bots, configfiles, init paths etc.
    botsinit.generalinit(configdir)

    if not check:
        # bots-engine should not run during the update
        try:
            engine_socket = botslib.check_if_other_engine_is_running()
        except OSError:
            print('Error: bots-engine is running (or another bots-updatedb). Nothing is changed.')
            sys.exit(3)
    try:
        code = update(check=check, backup_confirmed=backup_confirmed)
        if code == 0 and createsuperuser and not check:
            from django.core.management import call_command
            call_command('createsuperuser')
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print('Error in updating the database: %s: %s' % (exc.__class__.__name__, exc))
        code = 3
    finally:
        if not check:
            engine_socket.close()
    sys.exit(code)


if __name__ == '__main__':
    start()

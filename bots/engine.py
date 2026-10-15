"""Start bots-engine."""

import atexit
import logging
import os
import socket
import sys
import threading
import time
import traceback
import warnings

# bots-modules
from . import botsglobal
from . import botsinit
from . import botslib
from . import cleanup
from . import router
from .botslib import gettext as _
from .exceptions import BotsImportError


def logging_exit():
    """Shutown logging and move log file if requested"""
    logging.shutdown()
    if botsglobal.ini.get('settings', 'log_when', None) == 'report' \
            and getattr(botsglobal.currentrun, 'minta4query', None):
        # Not for classic logging, dailly or rotating
        # Rename engine.log with "botsglobal.currentrun.minta4query
        logfiles = [handler.baseFilename for handler in botsglobal.logger.handlers if hasattr(handler, 'baseFilename')]
        if logfiles and os.path.isfile(logfiles[0]):
            # os.replace: a log with that name can be there already (windows: os.rename gives an error)
            os.replace(
                logfiles[0],
                os.path.join(
                    botsglobal.ini.get('directories', 'logging'),
                    botsglobal.logger.name.replace(f"{__package__}.", ""),
                    str(botsglobal.currentrun.minta4query)
                )
            )


def start():
    """
    Start Bots engine; see run() for the exit codes.
    The engine always ends: if at the end something is still running (a thread started by a library or
    a user script) that is reported and the engine ends anyway.
    """
    try:
        run()
    except SystemExit as exc:
        code = exc.code
    else:
        code = 0
    leave(code)


def leave(code, wait=None):
    """End the engine with exit code 'code'."""
    if wait is None:
        wait = 30
        if botsglobal.ini:
            wait = botsglobal.ini.getint('settings', 'maxsecondsexit', 30)
    deadline = time.time() + wait
    busy = [thread for thread in threading.enumerate()
            if thread is not threading.main_thread() and not thread.daemon and thread.is_alive()]
    for thread in busy:
        thread.join(max(0, deadline - time.time()))
    busy = [thread for thread in busy if thread.is_alive()]
    if not busy:
        # the normal way: python runs what is registered to run at exit
        sys.exit(code)
    # python would wait for these threads for ever, with the database still locked for a next run.
    frames = sys._current_frames()  # pylint: disable=protected-access
    text = 'bots-engine is ready, but something is still running after %s seconds; bots-engine ends now.\n' % wait
    for thread in busy:
        text += 'Thread "%s":\n%s\n' % (
            thread.name, ''.join(traceback.format_stack(frames.get(thread.ident))) if thread.ident in frames else '?')
    try:
        if botsglobal.logger:
            botsglobal.logger.critical(text)
        else:
            sys.stderr.write(text)
    except Exception:  # pylint: disable=broad-exception-caught
        pass
    try:
        # remove database lock, close database, close log, etc
        atexit._run_exitfuncs()  # pylint: disable=protected-access
    finally:
        if isinstance(code, int):
            os._exit(code)  # pylint: disable=protected-access
        if code is not None:
            sys.stderr.write('%s\n' % code)
        os._exit(0 if code is None else 1)  # pylint: disable=protected-access


def run():
    """
    Run Bots engine

    sysexit codes:
    0: OK, no errors
    1: (system) errors incl parsing of command line arguments
    2: bots ran OK, but there are errors/process errors  in the run
    3: Database is locked, but "maxruntime" has not been exceeded.
    """
    # pylint: disable=too-many-locals, too-many-branches, too-many-statements, broad-exception-caught
    # ********command line arguments**************************
    usage = """
    This is "%(name)s" version %(version)s,
    part of Bots open source edi translator (https://bots-edi.org).
    Does the actual translations and communications; it's the workhorse.
    It does not have a fancy interface.

    Usage:
        %(name)s  [run-options] [config-option] [routes]
    Run-options (can be combined):
        --new                receive new edi files (default: if no run-option given: run as new).
        --resend             resend as indicated by user.
        --rereceive          rereceive as indicated by user.
        --automaticretrycommunication - automatically retry outgoing communication.
        --cleanup            remove older data from database.
    Config-option:
        -c<directory>        directory for configuration files (default: config).
    Routes: list of routes to run. Default: all active routes (in the database)

    """ % {
        'name': os.path.basename(sys.argv[0]),
        'version': botsglobal.version,
    }
    configdir = None
    commandspossible = ['--automaticretrycommunication', '--resend', '--rereceive', '--new']
    commandstorun = []
    # list with routes to run
    routestorun = []
    do_cleanup = False
    for arg in sys.argv[1:]:
        if arg.startswith('-c'):
            configdir = arg[2:]
            if not configdir:
                print('Error: configuration directory indicated, but no directory name.')
                sys.exit(1)
        elif arg in commandspossible:
            commandstorun.append(arg)
        elif arg == '--cleanup':
            do_cleanup = True
        elif arg in ['?', '/?', '-h', '--help'] or arg.startswith('-'):
            print(usage)
            sys.exit(0)
        else:
            # pick up names of routes to run
            routestorun.append(arg)
    if not commandstorun and not do_cleanup:
        # no command on command line, use new (default)
        commandstorun = ['--new']
    # sort commands
    commandstorun = [command[2:] for command in commandspossible if command in commandstorun]
    # ***********end handling command line arguments**************************

    # find locating of bots, configfiles, init paths etc.
    botsinit.generalinit(configdir)
    # set working directory to bots installation. advantage:
    #   when using relative paths it is clear that this point paths within bots installation.
    os.chdir(botsglobal.ini.get("directories", "botsenv"))

    # **************check if another instance of bots-engine is running/if port is free************
    try:
        engine_socket = botslib.check_if_other_engine_is_running()
    except socket.error:
        # logging is not started yet (the log is of the engine that runs): tell why nothing is done
        sys.stderr.write(
            'bots-engine does not run: another bots-engine is running for this environment (port %s is in use).\n'
            % botsglobal.ini.getint('settings', 'port', 28081))
        sys.exit(3)
    else:
        atexit.register(engine_socket.close)

    # **************initialise logging******************************
    botsglobal.logger = botsinit.initenginelogging(__name__)
    atexit.register(logging_exit)
    if botsglobal.ini.get('settings', 'log_when', None) != 'daily':
        botsglobal.logger.info(botslib.botsinfo_display())

    # **************connect to database**********************************
    try:
        botsinit.connect()
    except Exception as exc:
        botsglobal.logger.exception(
            _(
                'Could not connect to database. Database settings are in bots/config/settings.py.'
                ' Error: "%(exc)s".'
            ),
            {'exc': exc},
        )
        sys.exit(1)
    else:
        botsglobal.logger.info(_('Connected to database.'))
        atexit.register(botsglobal.db.close)
    # ************initialise user exits for the whole bots-engine*************************
    try:
        userscript, scriptname = botslib.botsimport('routescripts', 'botsengine')
    except BotsImportError:
        # userscript is not there; other errors like syntax errors are not catched
        userscript = scriptname = None
    # ***acceptance tests: initialiase acceptance user script******************************
    acceptance_userscript = acceptance_scriptname = None
    if botsglobal.ini.getboolean('acceptance', 'runacceptancetest', False):
        botsglobal.logger.info(
            _(
                'This run is an acceptance test - as indicated in option "runacceptancetest"'
                ' in bots.ini.'
            )
        )
        try:
            acceptance_userscript, acceptance_scriptname = botslib.botsimport(
                'routescripts', 'bots_acceptancetest'
            )
        except BotsImportError:
            botsglobal.logger.info(
                _(
                    'In acceptance test there is no script file "bots_acceptancetest.py"'
                    ' to check the results of the acceptance test.'
                )
            )

    # **************handle database lock****************************************
    # set a lock on the database;
    # if not possible, the database is locked:
    #   an earlier instance of bots-engine was terminated unexpectedly.
    if not botslib.database_has_engine_tables():
        botsglobal.logger.critical(_(
            'The database does not have the tables of bots-engine.\n'
            'Run "bots-updatedb" to create the tables in a new database or to update the database of bots 3.'
        ))
        sys.exit(3)
    if not botslib.set_database_lock():
        # for SQLite: do a integrity check on the database
        if botsglobal.connection.settings_dict["ENGINE"] == "django.db.backends.sqlite3":
            cursor = botsglobal.db.cursor()
            cursor.execute("""PRAGMA integrity_check""")
            result = cursor.fetchone()
            cursor.close()
            if result[0] != 'ok':
                warn = _(
                    '!Bots database is locked!\n'
                    'Bots did an integrity check on the database, but database was not OK.\n'
                    'Manual action is needed!\n'
                    'Bots has stopped processing EDI files.'
                )
                botsglobal.logger.critical(warn)
                botslib.sendbotserrorreport(_('[Bots severe error]Database is damaged'), warn)
                sys.exit(1)
        warn = _(
            '!Bots database is locked!\n'
            'Bots-engine has ended in an unexpected way during the last run.\n'
            'Most likely causes: sudden power-down, system crash, problems with disk I/O,'
            ' bots-engine terminated by user, etc.\n'
            'Bots will do an automatic crash recovery now.'
        )
        botsglobal.logger.critical(warn)
        botslib.sendbotserrorreport(_('[Bots severe error]Database is locked'), warn)
        # there is a database lock. Add a crashrecovery as first command to run.
        commandstorun.insert(0, 'crashrecovery')
    atexit.register(botslib.remove_database_lock)

    warnings.simplefilter('error', UnicodeWarning)

    # **************run the routes**********************************************
    # commandstorun determines the type(s) of run. eg: ['automaticretrycommunication','new']
    try:
        botslib.prepare_confirmrules()
        # in acceptance tests: run a user script before running eg to clean output directories
        botslib.tryrunscript(
            acceptance_userscript, acceptance_scriptname, 'pretest', routestorun=routestorun
        )
        botslib.tryrunscript(
            userscript, scriptname, 'pre', commandstorun=commandstorun, routestorun=routestorun
        )
        # detect if there has been some error.
        # Only used for correct exit() code
        errorinrun = 0
        first_command_2_run = True
        for command in commandstorun:
            # if multiple commands in run: reports etc are based on timestamp;
            # so there needs to be at least one second between these runs.
            if first_command_2_run:
                first_command_2_run = False
            else:
                time.sleep(1)
            botsglobal.logger.info(_('Run "%(command)s".'), {'command': command})
            # ************get list of routes to run*******************************
            if routestorun:
                use_routestorun = routestorun[:]
                botsglobal.logger.info(
                    _('Run routes from command line: "%(routes)s".'),
                    {"routes": str(use_routestorun)},
                )
            elif command == 'new':
                # fetch all active routes from database unless 'not in default run' or not active.
                use_routestorun = []
                for row in botslib.query(
                        """SELECT DISTINCT idroute
                           FROM routes
                           WHERE active=%(active)s
                           AND (notindefaultrun=%(notindefaultrun)s OR notindefaultrun IS NULL)
                           ORDER BY idroute """,
                        {'active': True, 'notindefaultrun': False}):
                    use_routestorun.append(row["idroute"])
                # in the order of the characters, as SQLite (and bots 3 on it) did: the collation of another
                # database may ignore case or punctuation and run the routes in another order
                use_routestorun.sort()
                botsglobal.logger.info(
                    _('Run active routes from database that are in default run: "%(routes)s".'),
                    {"routes": str(use_routestorun)},
                )
            else:
                # for command other than 'new': use all active routes.
                use_routestorun = []
                for row in botslib.query(
                        """SELECT DISTINCT idroute
                           FROM routes
                           WHERE active=%(active)s
                           ORDER BY idroute """,
                        {'active': True}):
                    use_routestorun.append(row["idroute"])
                use_routestorun.sort()      # see above
                botsglobal.logger.info(
                    _('Run all active routes from database: "%(routes)s".'),
                    {"routes": str(use_routestorun)},
                )
            # ************run routes for this command******************************
            botslib.tryrunscript(
                userscript, scriptname, 'pre' + command, routestorun=use_routestorun
            )
            errorinrun += router.rundispatcher(command, use_routestorun)
            botslib.tryrunscript(
                userscript, scriptname, 'post' + command, routestorun=use_routestorun
            )
            # *********finished running routes for this command****************************
        # *********finished all commands****************************************

        botslib.tryrunscript(
            userscript, scriptname, 'post', commandstorun=commandstorun, routestorun=routestorun
        )
        try:
            # in acceptance tests: run a user script.
            # no good reporting of errors/results in post-test script.
            # Reason: this is after automaticmaintence.
            botslib.tryrunscript(
                acceptance_userscript,
                acceptance_scriptname,
                'posttest',
                routestorun=routestorun,
            )
        except Exception as exc:
            print(str(exc))

        cleanup.cleanup(do_cleanup, userscript, scriptname)
    except Exception as exc:
        # of course this 'should' not happen.
        botsglobal.logger.exception(
            _("Severe error in bots system:\n%(exc)s"), {"exc": str(exc)}
        )
        sys.exit(1)
    else:
        if errorinrun:
            # indicate: error(s) in run(s)
            sys.exit(2)
        else:
            # OK
            sys.exit(0)


if __name__ == '__main__':
    start()

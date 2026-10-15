# -*- coding: utf-8 -*-
"""
Bots jobqueue: manage bots jobs by priority
There is the xml/rpc listner part, to add jobs in the queue
And some threads to run jobs in the queue.
"""

import logging
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from xmlrpc.server import SimpleXMLRPCServer

import defusedxml.xmlrpc

from . import botsglobal
from . import botsinit
from . import botslib
from .botsinit import LOG_LEVELS, STARTINFO
from .botslib import gettext as _


# security patch of xmlrpc lib
defusedxml.xmlrpc.monkey_patch()

STDOUT = STDERR = subprocess.PIPE

# Job args
PRIORITY = 0
JOBNUMBER = 1
TASK = 2

logger = logging.getLogger(__name__)

BOTS_TASKS = ['bots-engine']
# other tasks that can be run: as set in bots.ini, [jobqueue] authorized_tasks
AUTHORIZED_TASKS = BOTS_TASKS[:]
WINDOWS_EXTENSIONS = ('.exe', '.cmd', '.bat')


def task_name(program):
    """name of a program without directory; on windows: lower case and without .exe"""
    name = os.path.basename(str(program).replace('\\', '/'))
    if os.name == 'nt':
        name = name.lower()
        for extension in WINDOWS_EXTENSIONS:
            if name.endswith(extension):
                return name[:-len(extension)]
    return name


def task_paths(name):
    """
    The places a program of bots (eg bots-engine) is: via PATH, and next to the python that runs
    this server (the daemons are often started with an absolute path, without PATH being set).
    """
    found = []
    via_path = shutil.which(name)
    if via_path:
        found.append(via_path)
    here = os.path.dirname(os.path.abspath(sys.executable))
    for directory in (os.path.dirname(os.path.abspath(sys.argv[0])), here, os.path.join(here, 'Scripts'),
                      os.path.join(here, 'bin')):
        for extension in ('',) + (WINDOWS_EXTENSIONS if os.name == 'nt' else ()):
            candidate = os.path.join(directory, name + extension)
            if os.path.isfile(candidate):
                found.append(candidate)
    return found


def same_file(path1, path2):
    return os.path.normcase(os.path.realpath(path1)) == os.path.normcase(os.path.realpath(path2))


def is_authorized(program):
    """
    Only tasks of bots are run (and what is in bots.ini, [jobqueue] authorized_tasks):
    - the name of a bots program: 'bots-engine' (on windows also 'bots-engine.exe');
    - the path of that program as installed with this bots.
    """
    if not isinstance(program, str) or not program:
        return False
    if program in AUTHORIZED_TASKS:
        return True
    name = task_name(program)
    if name not in BOTS_TASKS:
        return False
    if os.path.basename(program.replace('\\', '/')) == program:
        # name without directory
        return True
    return any(same_file(program, known) for known in task_paths(name))


def program_to_run(program):
    """A program of bots given by name is run from where it is installed, also if PATH is not set."""
    if program not in AUTHORIZED_TASKS[len(BOTS_TASKS):] and task_name(program) in BOTS_TASKS \
            and os.path.basename(program.replace('\\', '/')) == program:
        paths = task_paths(task_name(program))
        if paths:
            return paths[0]
    return program


class Jobqueue:
    """
    handles the jobqueue.
    methodes can be called over xmlrpc (except the methods starting with '_')
    Jobs in the queue are lists: [priority, jobnumber, task].
    Order: priority 1 first, 9 last; within a priority: first in, first out.
    """

    def __init__(self):
        self.jobs = []
        # to assign unique sequential job-number
        self.jobcounter = 0
        # lock for the queue; launcher waits on this for a job
        self.condition = threading.Condition()
        self.accepting = True

    def addjob(self, task, priority=5):
        """
        Add job to queue. Returns:
        0 OK; 2 no task; 3 task not allowed; 4 job is already in the queue; 5 priority is not a number;
        6 the server does not run jobs (stopping, or stopped after errors).
        """
        if not task or not isinstance(task, (list, tuple)):
            logger.error(_('No task specified.'))
            return 2
        task = [str(arg) for arg in task]
        if task[0] == 'isup':
            logger.info(_('%s is up.'), __name__)
            return 0
        # Filter dangerous task, as non-bots-tasks might be started ...
        # authorise only bots tasks.
        if not is_authorized(task[0]):
            logger.error(_('Invalid task received: %(task)s'), {'task': task})
            return 3
        try:
            priority = int(priority)
        except (TypeError, ValueError):
            logger.error(_('Invalid priority "%(priority)s" for task: %(task)s'), {'priority': priority, 'task': task})
            return 5
        with self.condition:
            if not self.accepting:
                logger.error(_('Job not accepted, jobqueue-server does not run jobs: %(task)s'), {'task': task})
                return 6
            # first check if job already in queue
            for job in self.jobs:
                if job[TASK] == task:
                    if job[PRIORITY] != priority:
                        job[PRIORITY] = priority
                        self.jobs.sort()
                        logger.info(
                            _('Duplicate job, changed priority to %(priority)s: %(task)s'),
                            {'priority': priority, 'task': task},
                        )
                        return 0
                    logger.warning(_('Duplicate job not added: %(task)s'), {'task': task})
                    return 4
            # add the job
            self.jobcounter += 1
            self.jobs.append([priority, self.jobcounter, task])
            # priority 1 first; same priority: lowest job number (oldest) first
            self.jobs.sort()
            logger.info(
                _('Added job %(job)s, priority %(priority)s: %(task)s'),
                {'job': self.jobcounter, 'priority': priority, 'task': task},
            )
            self.condition.notify()
        return 0

    def listjobs(self):
        """List jobs queue"""
        with self.condition:
            return [list(job) for job in self.jobs] or 0

    def clearjobq(self):
        """Clear jobs queue"""
        with self.condition:
            del self.jobs[:]
        logger.info(_('Job queue cleared.'))
        return 0

    def _get(self):
        """Wait for a job; returns the job to run now, or None if the server stops."""
        with self.condition:
            while self.accepting and not self.jobs:
                self.condition.wait()
            if not self.accepting:
                return None
            return self.jobs.pop(0)

    def _stop(self):
        """No more jobs are accepted or started. Returns the jobs that were waiting."""
        with self.condition:
            self.accepting = False
            waiting, self.jobs = self.jobs, []
            self.condition.notify_all()
        return waiting


def kill_job(proc):
    """Kill a job with the processes it started."""
    try:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(proc.pid)], capture_output=True, check=False)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.error(_('Error in killing job: %(exc)s'), {'exc': exc})
    try:
        proc.kill()
    except Exception:  # pylint: disable=broad-exception-caught
        pass


def run_job(job, maxruntime):
    """
    Run one job, log what it wrote. Returns exit code of the job.
    Raises an exception if the job could not be started.
    """
    jobnumber, task_to_run = job[JOBNUMBER], list(job[TASK])
    task_to_run[0] = program_to_run(task_to_run[0])
    logger.log(
        LOG_LEVELS['START'], _('Starting job %(jobnumber)s: %(task_to_run)s'),
        {'jobnumber': jobnumber, 'task_to_run': task_to_run})
    starttime = time.time()
    # a job is the leader of its own group of processes: on timeout the whole group can be killed
    if os.name == 'nt':
        own_group = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP}
    else:
        own_group = {'start_new_session': True}
    with subprocess.Popen(task_to_run, stdout=STDOUT, stderr=STDERR, stdin=subprocess.DEVNULL, **own_group) as proc:
        try:
            outs, errs = proc.communicate(timeout=maxruntime * 60)
        except subprocess.TimeoutExpired:
            info = {'jobnumber': jobnumber, 'maxruntime': maxruntime, 'task_to_run': task_to_run}
            logger.error(_('Job %(jobnumber)s exceeded maxruntime of %(maxruntime)s minutes'), info)
            botslib.sendbotserrorreport(
                _('[Bots Job Queue] - Job exceeded maximum runtime'),
                _('Job %(jobnumber)s exceeded maxruntime of %(maxruntime)s minutes:\n %(task_to_run)s') % info)
            if botsglobal.ini.getboolean("jobqueue", "killjobsintimeout", False):
                logger.info(_('Killing job %(jobnumber)s: %(task_to_run)s'), info)
                kill_job(proc)
                try:
                    outs, errs = proc.communicate(timeout=30)
                except subprocess.TimeoutExpired:
                    # a process started by the job still has the output open: do not wait for it
                    outs = errs = b''
                    logger.error(_('Job %(jobnumber)s: could not read the output after killing the job.'), info)
            else:
                outs, errs = proc.communicate()
        returncode = proc.returncode
    time_taken = time.time() - starttime
    if returncode != 0:
        logger.error(
            _('job %(jobnumber)s, exit with code %(returncode)s'), {'jobnumber': jobnumber, 'returncode': returncode})
    if errs:
        errs = errs.decode(errors='replace') if isinstance(errs, bytes) else errs
        if returncode != 0:
            logger.error("%s%s", os.linesep, errs)
        else:
            logger.log(LOG_LEVELS["STDERR"], "%s %s", os.linesep, errs)
    if outs:
        outs = outs.decode(errors='replace') if isinstance(outs, bytes) else outs
        logger.log(LOG_LEVELS['STDOUT'], "%s %s", os.linesep, outs)
    logger.log(
        LOG_LEVELS['DONE'],
        _('Finished job %(jobnumber)s, elapsed time: %(time_taken)s, exit code %(returncode)s'),
        {"jobnumber": jobnumber, "time_taken": time_taken, "returncode": returncode},
    )
    return returncode


def launcher(jobqueue, maxruntime, on_fatal=None):
    """
    Bots jobqueue launcher: runs the jobs in the queue, one at a time.
    After 10 jobs in a row that could not be started the server stops running and accepting jobs.
    """
    logger.debug(_('Job launcher running'))
    nko = 0
    while True:
        job = jobqueue._get()  # pylint: disable=protected-access
        if job is None:
            logger.debug(_('Job launcher stopped'))
            return
        try:
            run_job(job, maxruntime)
            nko = 0
        except Exception as exc:  # pylint: disable=broad-exception-caught
            nko += 1
            info = {"jobnumber": job[JOBNUMBER], "task_to_run": job[TASK], "exc": exc}
            logger.error(_("Error starting job %(jobnumber)s: %(exc)s"), info)
            botslib.sendbotserrorreport(
                _('[Bots Job Queue] - Error starting job'),
                _('Error starting job %(jobnumber)s:\n %(task_to_run)s\n\n %(exc)s') % info,
            )
            if nko >= 10:
                logger.error(_(
                    'More than 10 consecutive errors in the bots-jobqueueserver, '
                    'shutting down now'
                ))
                botslib.sendbotserrorreport(
                    _('[Bots Job Queue] bots-jobqueueserver has stopped'),
                    _('More than 10 consecutive errors occured in the bots-jobqueueserver, '
                      'so jobqueue-server is stopped now.')
                )
                for waiting in jobqueue._stop():  # pylint: disable=protected-access
                    logger.error(_('Job %(jobnumber)s is not run: %(task)s'), {'jobnumber': waiting[JOBNUMBER], 'task': waiting[TASK]})
                if on_fatal:
                    on_fatal()
                return


def start():
    """
    Start Bots Jobqueue
    """
    usage = """
    This is "%(name)s" version %(version)s,
    part of Bots open source edi translator (https://bots-edi.org).

    Server program that ensures only a single bots-engine runs at any time,
    and no engine run requests are lost/discarded.
    Each request goes to a queue and is run in sequence when the previous run completes.

    # Use of the job queue is optional and must be configured in bots.ini (jobqueue section):
        enabled = True

    # To authorize custom task to be launched, add in bots.ini (jobqueue section):
        authorized_tasks = /path/bin/custom /path/bin/custom2

    # Kill Jobs in timeout (jobs exceeded maxruntime)
        killjobsintimeout = False

    Usage:
        %(name)s -c<directory>

    Options:
        -c<directory>   directory for configuration files (default: config).

    """ % {
        'name': os.path.basename(sys.argv[0]),
        'version': botsglobal.version,
    }

    # ***command line arguments**************************
    configdir = None
    for arg in sys.argv[1:]:
        if arg.startswith('-c'):
            configdir = arg[2:]
            if not configdir:
                print(_('Error: configuration directory indicated, but no directory name.'))
                sys.exit(1)
        else:
            print(usage)
            sys.exit(0)
    # ***end handling command line arguments**************************

    # find locating of bots, configfiles, init paths etc.
    botsinit.generalinit(configdir)
    if not botsglobal.ini.getboolean('jobqueue', 'enabled', False):
        print(_('Error: bots jobqueue is not enabled in %(configdir)s/bots.ini') % {
            'configdir': botsglobal.ini.get('directories', 'config')})
        sys.exit(1)

    botsglobal.logger = botsinit.initserverlogging(__name__)
    # atexit.register(logging.shutdown)
    logger.log(STARTINFO, _('Starting ...'))
    logger.log(
        STARTINFO,
        _('configdir: "%(configdir)s".'),
        {'configdir': botsglobal.ini.get('directories', 'config')},
    )
    # AUTHORIZED_TASKS in bots.ini
    if botsglobal.ini.get('jobqueue', 'authorized_tasks', False):
        authorized_tasks = botsglobal.ini.get('jobqueue', 'authorized_tasks').strip()
        AUTHORIZED_TASKS.extend(filter(
            bool, authorized_tasks.replace(',', ' ').replace(';', ' ').split(' ')))
    logger.debug('AUTHORIZED_TASKS: %s', AUTHORIZED_TASKS)
    for name in BOTS_TASKS:
        logger.log(STARTINFO, _('%(name)s is run from: %(paths)s'), {'name': name, 'paths': task_paths(name)[:1] or '?'})

    # Init job queue
    jobqueue = Jobqueue()
    port = botsglobal.ini.getint('jobqueue', 'port', 28082)
    # the main thread is the xmlrpc server:
    # all adding, getting etc for jobqueue is done via xmlrpc.
    server = SimpleXMLRPCServer(('127.0.0.1', port), logRequests=False)
    server.register_instance(jobqueue)
    state = {'exitcode': 0}

    def stop_server(exitcode=0):
        """stop listening; from another thread than the one that serves"""
        state['exitcode'] = max(state['exitcode'], exitcode)
        threading.Thread(target=server.shutdown, daemon=True).start()

    # start launcher thread. One job at a time: 2 engines can not run at the same time in one environment.
    maxruntime = botsglobal.ini.getint('settings', 'maxruntime', 60)
    if botsglobal.ini.getint('jobqueue', 'nr_threads', 1) != 1:
        logger.warning(_('bots.ini, [jobqueue] nr_threads is not used: jobs are run one at a time.'))
    launcher_thread = threading.Thread(
        name='launcher', target=launcher, args=(jobqueue, maxruntime, lambda: stop_server(1)), daemon=True)
    launcher_thread.start()

    # stop in an orderly way on SIGTERM (eg systemctl stop) and Ctrl-C
    def handle_signal(signum, frame):  # pylint: disable=unused-argument
        logger.info(_('Received signal to stop.'))
        stop_server(0)
    for name in ('SIGTERM', 'SIGINT', 'SIGBREAK'):
        if hasattr(signal, name):
            try:
                signal.signal(getattr(signal, name), handle_signal)
            except (ValueError, OSError):
                pass

    logger.log(
        STARTINFO,
        _('Listening xmlrpc request on port: "%(port)s".'),
        {'port': port},
    )
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        sys.stderr.write(os.linesep)
    server.server_close()

    # no new jobs; the job that runs can finish; tell which jobs are not run
    logger.info(_('Exiting ...'))
    for waiting in jobqueue._stop():  # pylint: disable=protected-access
        logger.warning(_('Job %(jobnumber)s is not run: %(task)s'), {'jobnumber': waiting[JOBNUMBER], 'task': waiting[TASK]})
    stopwait = botsglobal.ini.getint('jobqueue', 'stopwait', 60)
    if launcher_thread.is_alive():
        logger.info(_('Waiting (max %(stopwait)s seconds) for the job that runs.'), {'stopwait': stopwait})
        launcher_thread.join(stopwait)
        if launcher_thread.is_alive():
            logger.error(_('A job is still running; jobqueue-server stops.'))
            state['exitcode'] = max(state['exitcode'], 1)
    logger.info(_('Stopped.'))
    logging.shutdown()
    sys.exit(state['exitcode'])


if __name__ == '__main__':
    start()

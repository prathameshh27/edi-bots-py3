"""Job queue (order, accepted tasks, launcher) and the matching of events in the directory monitor."""
import os
import sys
import threading
import time

import pytest


@pytest.fixture
def jobqueueserver(botsenv):
    from bots import jobqueueserver as module
    before = list(module.AUTHORIZED_TASKS)
    yield module
    module.AUTHORIZED_TASKS[:] = before


# ---------------------------------------------------------------- queue

def test_order_is_priority_then_first_in_first_out(jobqueueserver):
    queue = jobqueueserver.Jobqueue()
    for name, priority in (('A', 5), ('B', 5), ('C', 5), ('URGENT', 1), ('LOW', 9)):
        assert queue.addjob(['bots-engine', name], priority) == 0
    assert [job[2][1] for job in queue.listjobs()] == ['URGENT', 'A', 'B', 'C', 'LOW']
    assert [queue._get()[2][1] for _ in range(5)] == ['URGENT', 'A', 'B', 'C', 'LOW']
    assert queue.listjobs() == 0


def test_addjob_return_codes(jobqueueserver):
    queue = jobqueueserver.Jobqueue()
    assert queue.addjob([], 5) == 2
    assert queue.addjob(['isup'], 5) == 0 and queue.listjobs() == 0
    assert queue.addjob(['format', 'c:'], 5) == 3
    assert queue.addjob(['bots-engine', 'route'], 'high') == 5
    assert queue.addjob(['bots-engine', 'route'], 5) == 0
    assert queue.addjob(['bots-engine', 'route'], 5) == 4               # duplicate
    assert queue.addjob(['bots-engine', 'route'], 1) == 0               # duplicate: priority is changed
    assert queue.addjob(['bots-engine', 'other'], '3') == 0             # a number as text is accepted
    assert [(job[0], job[2][1]) for job in queue.listjobs()] == [(1, 'route'), (3, 'other')]
    # the queue still works after the errors above (no lock is left behind)
    assert queue.clearjobq() == 0 and queue.listjobs() == 0
    assert [job[2] for job in queue._stop()] == []
    assert queue.addjob(['bots-engine', 'route'], 5) == 6
    assert queue._get() is None


def test_which_tasks_are_accepted(jobqueueserver, tmp_path):
    accepted = jobqueueserver.is_authorized
    assert accepted('bots-engine')
    assert accepted('bots-engine.exe') == (os.name == 'nt')
    assert not accepted('bots-engine2') and not accepted('python') and not accepted('') and not accepted(None)
    # a program with the right name in another place is not accepted
    other = tmp_path / ('bots-engine.exe' if os.name == 'nt' else 'bots-engine')
    other.write_text('not the engine')
    assert not accepted(str(other))
    # ... unless it is the one found via PATH, or set in bots.ini
    jobqueueserver.AUTHORIZED_TASKS.append(str(other))
    assert accepted(str(other))


# ---------------------------------------------------------------- launcher

def python_job(code, number=1):
    return [5, number, [sys.executable, '-c', code]]


def test_job_output_that_is_not_utf8(jobqueueserver):
    jobqueueserver.AUTHORIZED_TASKS.append(sys.executable)
    code = "import sys; sys.stdout.buffer.write(b'caf\\xe9 \\xff\\xfe'); sys.stderr.buffer.write(b'\\xe9'); sys.exit(3)"
    assert jobqueueserver.run_job(python_job(code), maxruntime=1) == 3


def test_job_that_runs_too_long_is_killed_with_its_children(jobqueueserver, tmp_path):
    from bots import botsglobal
    marker = str(tmp_path / 'child_still_running')
    child = ("import time, sys\n"
             "time.sleep(8)\n"
             "open(sys.argv[1], 'w').close()\n")
    parent = ("import subprocess, sys, time\n"
              "subprocess.Popen([sys.executable, '-c', %r, %r])\n"
              "time.sleep(60)\n" % (child, marker))
    botsglobal.ini.set('jobqueue', 'killjobsintimeout', 'True')
    try:
        start = time.time()
        code = jobqueueserver.run_job(python_job(parent), maxruntime=2.0 / 60)
    finally:
        botsglobal.ini.set('jobqueue', 'killjobsintimeout', 'False')
    assert code != 0
    assert time.time() - start < 40, 'the queue does not wait for what the job left behind'
    time.sleep(9)
    assert not os.path.exists(marker), 'the process started by the job is killed too'


def test_launcher_stops_accepting_after_ten_jobs_that_can_not_start(jobqueueserver):
    queue = jobqueueserver.Jobqueue()
    notthere = os.path.join(os.path.dirname(sys.executable), 'this-program-does-not-exist')
    jobqueueserver.AUTHORIZED_TASKS.append(notthere)
    for number in range(12):
        assert queue.addjob([notthere, str(number)], 5) == 0
    fatal = []
    thread = threading.Thread(target=jobqueueserver.launcher, args=(queue, 1, lambda: fatal.append(1)), daemon=True)
    thread.start()
    thread.join(30)
    assert not thread.is_alive() and fatal == [1]
    assert queue.listjobs() == 0
    assert queue.addjob(['bots-engine', 'route'], 5) == 6, 'jobs are refused, not accepted and forgotten'


def test_launcher_continues_after_a_job_that_can_not_start(jobqueueserver, tmp_path):
    queue = jobqueueserver.Jobqueue()
    notthere = os.path.join(os.path.dirname(sys.executable), 'this-program-does-not-exist')
    jobqueueserver.AUTHORIZED_TASKS.extend([notthere, sys.executable])
    marker = tmp_path / 'second_job_ran'
    assert queue.addjob([notthere], 1) == 0
    assert queue.addjob([sys.executable, '-c', 'open(%r, "w").close()' % str(marker)], 5) == 0
    thread = threading.Thread(target=jobqueueserver.launcher, args=(queue, 1), daemon=True)
    thread.start()
    for _ in range(100):
        if marker.exists():
            break
        time.sleep(0.2)
    queue._stop()
    thread.join(10)
    assert marker.exists() and not thread.is_alive()


# ---------------------------------------------------------------- dirmonitor: which events are for a watch

@pytest.fixture
def dirmonitor(botsenv):
    if os.name == 'posix':
        pytest.importorskip('pyinotify')
    from bots import dirmonitor as module
    return module


def test_event_matches(dirmonitor, tmp_path):
    watched = tmp_path / 'in'
    (watched / 'sub' / 'deeper').mkdir(parents=True)
    (tmp_path / 'in_other').mkdir()
    flat = {'path': str(watched), 'filemask': '*.edi', 'rec': False}
    recursive = dict(flat, rec=True)
    match = dirmonitor.event_matches
    # name relative to the watched directory (windows) and absolute (linux)
    assert match(flat, 'order.edi') and match(flat, str(watched / 'order.edi'))
    assert not match(flat, 'order.txt') and not match(flat, str(watched / 'order.txt'))
    # sub-directories: only for a recursive watch
    for name in (os.path.join('sub', 'order.edi'), str(watched / 'sub' / 'deeper' / 'order.edi')):
        assert not match(flat, name) and match(recursive, name), name
    # a directory with a name that starts the same is another directory
    assert not match(recursive, str(tmp_path / 'in_other' / 'order.edi'))
    # the watched path as it can be written in bots.ini or in a channel
    for spelling in (str(watched) + os.sep, str(tmp_path / 'in_other' / '..' / 'in'),
                     str(watched).replace(os.sep, os.sep * 2 if os.name == 'posix' else '/')):
        assert match(dict(flat, path=spelling), str(watched / 'order.edi')), spelling
    # wildcards in the path
    pattern = dict(flat, path=str(watched / '*'))
    assert dirmonitor.watch_root(pattern['path']) == str(watched)
    assert match(pattern, str(watched / 'sub' / 'order.edi')) and match(pattern, os.path.join('sub', 'order.edi'))
    assert not match(pattern, str(watched / 'order.edi'))

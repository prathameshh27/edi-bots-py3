"""Errors of the engine that need a real run (found by reading the code, 2026-10-18; all came from bots 3)."""
import os
import stat
import sys
import textwrap

import pytest

PAYLOAD = b"UNB+UNOA:2+SENDER+RECEIVER+260101:1200+1'UNZ+0+1'"


def engine_log(botsrun):
    with open(os.path.join(botsrun.root, 'engine.log'), encoding='utf8', errors='replace') as f:
        return f.read()


def passthrough_route(botsrun, name, files, **out_channel):
    """a route that passes files from a folder to a folder; returns both folders"""
    src, out = botsrun.path('src_' + name), botsrun.path('out_' + name)
    for filename in files:
        with open(os.path.join(src, filename), 'wb') as f:
            f.write(PAYLOAD)
    botsrun.configure(
        channels=[dict(idchannel=name + '_in', inorout='in', type='file', path=src, filename='*.edi', remove=True),
                  dict(idchannel=name + '_out', inorout='out', type='file', path=out, filename='{infile}',
                       **out_channel)],
        routes=[dict(idroute=name, seq=1, active=True, fromchannel=name + '_in', tochannel=name + '_out',
                     translateind=2)])
    return src, out


def communication_script(botsrun, idchannel, text):
    directory = os.path.join(botsrun.envdir, 'usersys', 'communicationscripts')
    with open(os.path.join(directory, idchannel + '.py'), 'w', encoding='utf8') as f:
        f.write(textwrap.dedent(text))


def test_an_error_in_the_set_up_of_a_run_makes_the_run_fail(botsrun):
    """bots 3: the error was caught and counted as 0 errors: exit code 0, no report, no error mail"""
    assert botsrun.engine() == 0
    botsrun.side('sql', 'DROP TABLE filereport')        # rereceive starts by reading it
    assert botsrun.engine('--rereceive') == 2
    assert 'filereport' in engine_log(botsrun)


def test_a_received_file_that_can_not_be_removed_does_not_stop_the_others(botsrun):
    """bots 3: the first file that could not be removed from its folder ended the channel; the files after it
    were not received in that run"""
    if os.name != 'nt' and os.geteuid() == 0:
        pytest.skip('root can remove files from a folder without write permission')
    src, out = passthrough_route(botsrun, 'locked', ['a.edi', 'b.edi'])
    locked = os.path.join(src, 'a.edi')
    if os.name == 'nt':
        os.chmod(locked, stat.S_IREAD)                  # windows: a read-only file can not be removed
    else:
        os.chmod(src, stat.S_IREAD | stat.S_IEXEC)      # posix: no file can be removed from this folder
    try:
        botsrun.engine()
    finally:
        os.chmod(locked, stat.S_IREAD | stat.S_IWRITE)
        os.chmod(src, stat.S_IRWXU)
    assert sorted(os.listdir(out)) == ['a.edi', 'b.edi']
    assert 'could not be removed' in engine_log(botsrun)


def test_a_failing_send_leaves_no_lock_on_the_channel(botsrun):
    """bots 3: when sending failed in a communication script, disconnect did not run: the lock file stayed and
    blocked the channel until someone removed it"""
    _src, out = passthrough_route(botsrun, 'failsend', ['a.edi'], lockname='bots.lock')
    communication_script(botsrun, 'failsend_out', '''
        from bots import communication

        class file(communication.file):
            def outcommunicate(self):
                raise RuntimeError('sending fails on purpose')
    ''')
    botsrun.engine()
    assert 'sending fails on purpose' in engine_log(botsrun)
    assert not os.path.exists(os.path.join(out, 'bots.lock'))

"""Errors of the engine found by reading the code (2026-10-18): each test shows one, the fix makes it pass.

All of them came with the code from bots 3.
"""
import os
import types

import pytest

from bots.botsconfig import DONE, ERROR, FILEIN, MERGED, OK, PARSED, TRANSLATED


def new_ta(**fields):
    from bots import botslib
    return botslib.NewTransaction(**fields)


def ta_row(idta):
    from bots import botslib
    rows = list(botslib.query(
        'SELECT idta, status, statust, errortext, child FROM ta WHERE idta=%(idta)s', {'idta': idta}))
    return dict(rows[0])


def children(idta):
    from bots import botslib
    return [dict(row) for row in botslib.query(
        'SELECT idta, status, statust, errortext FROM ta WHERE parent=%(idta)s', {'idta': idta})]


# ---------------------------------------------------------------- translating and enveloping

def test_a_file_that_can_not_be_read_is_an_error_of_that_file(botsenv):
    """bots 3: the error handler used the edi file that was never made (NameError), and the rest of the route's
    files were skipped"""
    from bots import transform
    ta = new_ta(status=FILEIN, statust=OK, idroute='ut_unreadable', editype='nosuchtype', messagetype='x',
                filename='nofile')
    row = dict(idta=ta.idta, filename='nofile', filesize=0, frompartner='', topartner='', messagetype='x',
               testindicator='', editype='nosuchtype', charset='', alt='', fromchannel='', frommail='', tomail='')
    routedict = {'idroute': 'ut_unreadable', 'command': 'new', 'translateind': 1}
    transform._translate_one_file(row, routedict, TRANSLATED, None, None)
    parsed = children(ta.idta)
    assert [(p['status'], p['statust']) for p in parsed] == [(PARSED, ERROR)]
    assert 'Unknown editype' in parsed[0]['errortext']


def test_an_enveloping_error_is_on_the_message_that_failed(botsenv, monkeypatch):
    """bots 3: the error went to the file of the previous message, or the handler itself failed (NameError)"""
    from bots import botslib, envelope
    process = botslib.NewProcess('ut_envelope_error')
    message = new_ta(status=TRANSLATED, statust=OK, idroute='ut_envelope_error', merge=False, editype='fixed',
                     messagetype='x', filename='nofile')

    def copyta_fails(self, status, **ta_info):
        raise RuntimeError('database is gone')

    monkeypatch.setattr(botslib.OldTransaction, 'copyta', copyta_fails)
    envelope.mergemessages(TRANSLATED, MERGED, 'ut_envelope_error', rootidta=process.idta - 1)
    monkeypatch.undo()
    process.update(statust=DONE)
    row = ta_row(message.idta)
    assert row['statust'] == ERROR
    assert 'database is gone' in row['errortext']


def test_messages_with_an_empty_value_in_a_merge_column_are_merged(botsenv):
    """bots 3: a column that is NULL (here: envelope, set to None by a mapping) matched no message, the messages
    stayed TRANSLATED and only the log said so"""
    from bots import botslib, envelope
    process = botslib.NewProcess('ut_merge_null')
    messages = [new_ta(status=TRANSLATED, statust=OK, idroute='ut_merge_null', merge=True, editype='fixed',
                       messagetype='x', charset='us-ascii', testindicator='', envelope='', rsrv3='')
                for _ in range(2)]
    for message, text in zip(messages, ('first\n', 'second\n')):
        filename = str(message.idta)
        message.update(filename=filename)
        with botslib.opendata(filename, 'w', 'us-ascii') as f:
            f.write(text)
        botslib.changeq('UPDATE ta SET envelope=NULL WHERE idta=%(idta)s', {'idta': message.idta})
    envelope.mergemessages(TRANSLATED, MERGED, 'ut_merge_null', rootidta=process.idta - 1)
    process.update(statust=DONE)
    rows = [ta_row(message.idta) for message in messages]
    assert [row['statust'] for row in rows] == [DONE, DONE]
    assert rows[0]['child'] and rows[0]['child'] == rows[1]['child']
    assert ta_row(rows[0]['child'])['statust'] == OK


# ---------------------------------------------------------------- user scripts

def test_an_error_inside_a_user_script_is_not_taken_for_a_missing_script(botsenv):
    """bots 3: a script that imports a library that is not installed counted as 'no script' (and for a
    communication script, bots' own channel class ran instead, without a word)"""
    from bots import botslib
    from bots.exceptions import BotsImportError, ScriptImportError
    folder = os.path.join(botsenv, 'usersys', 'communicationscripts')
    with open(os.path.join(folder, 'ut_needs_library.py'), 'w', encoding='utf8') as f:
        f.write('import no_such_library_for_bots_unittest\n')
    for _ in range(2):      # also the second time: not remembered as missing
        with pytest.raises(ScriptImportError):
            botslib.botsimport('communicationscripts', 'ut_needs_library')
    with pytest.raises(BotsImportError):
        botslib.botsimport('communicationscripts', 'ut_no_such_script')


# ---------------------------------------------------------------- database and counters

def test_a_new_counter_keeps_the_value_it_is_given(botsenv):
    """bots 3: a new counter stored 1, not the value given; automatic retry did nothing in its first two runs
    and the daily clean-up ran twice on the first day"""
    from bots import botslib
    assert botslib.unique('ut_given', updatewith=500) == 1      # 1: the counter is new
    assert botslib.unique('ut_given', updatewith=600) == 500


def test_the_run_counter_starts_again_after_the_largest_number(botsenv, monkeypatch):
    from bots import botsglobal, botslib
    monkeypatch.setattr(botsglobal, 'ut_wrapbots_1_8_4_9_6', botslib.MAXINT, raising=False)
    assert botslib.unique_runcounter('ut_wrap') == 0
    assert botslib.unique_runcounter('ut_wrap') == 1


class FailingCursor:
    def __init__(self, database):
        self.database = database

    def execute(self, *args):
        raise RuntimeError('bad statement')

    def close(self):
        self.database.closed += 1


class FailingDatabase:
    def __init__(self):
        self.rolled_back = False
        self.closed = 0

    def cursor(self):
        return FailingCursor(self)

    def rollback(self):
        self.rolled_back = True

    def commit(self):
        pass


@pytest.mark.parametrize('function', ['query', 'insertta', 'changeq'])
def test_a_failing_statement_rolls_back_and_closes_its_cursor(botsenv, monkeypatch, function):
    """bots 3: query and insertta did not roll back (PostgreSQL then refuses every later statement), and the
    cursor was left open"""
    from bots import botsglobal, botslib
    database = FailingDatabase()
    monkeypatch.setattr(botsglobal, 'db', database)
    with pytest.raises(RuntimeError):
        list(getattr(botslib, function)('SELECT 1') or [])
    assert database.rolled_back
    assert database.closed == 1


def test_confirm_rules_read_twice_are_not_doubled(botsenv):
    from bots import botsglobal, botslib, models
    models.confirmrule.objects.create(active=True, confirmtype='send-x12-997', ruletype='all')
    botslib.prepare_confirmrules()
    botslib.prepare_confirmrules()
    assert len(botsglobal.confirmrules) == 1


def test_the_process_stack_stays_right_when_recording_a_process_fails(botsenv, monkeypatch):
    from bots import botslib
    depth = len(botslib._Transaction.processlist)
    process = botslib.NewProcess('ut_stack')

    def update_fails(self, **ta_info):
        raise RuntimeError('database is gone')

    monkeypatch.setattr(botslib.NewTransaction, 'update', update_fails)
    with pytest.raises(RuntimeError):
        process.update(statust=DONE)
    assert len(botslib._Transaction.processlist) == depth


# ---------------------------------------------------------------- communication

def test_the_logger_pipe_writes_to_the_engine_log(botsenv, monkeypatch):
    """the default logger was fixed when the module was imported, when there was no logger yet"""
    from bots import botsglobal, communication
    lines = []
    monkeypatch.setattr(botsglobal, 'logger', types.SimpleNamespace(log=lambda level, text: lines.append(text)))
    pipe = communication.LoggerPipe()
    pipe.write('hello\n')
    assert lines == ['hello']


@pytest.mark.parametrize('username, secret, address', [
    ('user', 'pw', 'http://user:pw@example.com:8000'),
    ('user', ':pw', 'http://user:pw@example.com:8000'),     # as some wrote it for bots 3
    ('user', '', 'http://user@example.com:8000'),
    ('', '', 'http://example.com:8000'),
])
def test_xmlrpc_address_has_user_and_password_apart(monkeypatch, username, secret, address):
    """bots 3 put the password straight after the user name, without ':'"""
    import xmlrpc.client
    from bots import communication
    seen = []

    class Proxy:
        def __init__(self, uri):
            seen.append(uri)

        def __getattr__(self, name):
            return name

    monkeypatch.setattr(xmlrpc.client, 'ServerProxy', Proxy)
    session = types.SimpleNamespace(channeldict=dict(username=username, secret=secret, host='example.com',
                                                     port=8000, path='call'))
    communication.xmlrpc.connect(session)
    assert seen == [address]
    assert 'pw' not in session.filename

"""Behaviour that existing bots 3.x grammars, mappings and scripts rely on."""
import os

import pytest

from helpers import new_out, parse, records, write_grammar, written, written_json

CSV_GRAMMAR = '''
    from bots.botsconfig import *
    syntax = {'field_sep': ',', 'quote_char': '"', 'charset': 'utf-8', %s}
    structure = [{ID: 'HEA', MIN: 1, MAX: 9999}]
    recorddefs = {
        'HEA': [
            ['BOTSID', 'M', 3, 'A'],
            ['NAME', 'C', 35, 'AN'],
            ['QTY', 'C', 16.3, 'R'],
            ['DATE', 'C', 8, 'D'],
            ['PRICE', 'C', 16.2, 'R'],
        ],
    }
'''
JSON_GRAMMAR = '''
    from bots.botsconfig import *
    syntax = {%s}
    structure = [{ID: 'order', MIN: 1, MAX: 9999, LEVEL: [{ID: 'line', MIN: 0, MAX: 9999}]}]
    recorddefs = {
        'order': [['BOTSID', 'M', 20, 'A'], ['nr', 'C', 35, 'AN']],
        'line': [['BOTSID', 'M', 20, 'A'], ['item', 'C', 35, 'AN']],
    }
'''


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    write_grammar('csv', 'ut_strip', CSV_GRAMMAR % '')
    write_grammar('csv', 'ut_nostrip', CSV_GRAMMAR % "'strip_value': False")
    write_grammar('json', 'ut_orders', JSON_GRAMMAR % '')
    write_grammar('json', 'ut_orders_list', JSON_GRAMMAR % "'force_list': True")
    write_grammar('jsonnocheck', 'ut_free', "from bots.botsconfig import *\nsyntax = {}\n")


# ---------------------------------------------------------------- names user scripts use

def test_exceptions_and_constants_reachable_through_botslib():
    from bots import botslib, exceptions
    for name in ('BotsError', 'BotsImportError', 'CodeConversionError', 'CommunicationError', 'CommunicationInError',
                 'CommunicationOutError', 'EanError', 'FileTooLargeError', 'GotoException', 'GrammarError',
                 'GrammarPartMissing', 'InMessageError', 'LockedFileError', 'MappingFormatError', 'MappingRootError',
                 'MessageError', 'MessageRootError', 'OutMessageError', 'PanicError', 'PersistError', 'PluginError',
                 'ScriptError', 'ScriptImportError', 'TraceError', 'TranslationNotFoundError'):
        assert getattr(botslib, name) is getattr(exceptions, name), name
    assert botslib.FILEIN == 220 and botslib.EXTERNOUT == 520 and botslib.TRANSLATED == 330
    assert callable(botslib.txtexc) and callable(botslib.safe_unicode)


def test_botserror_message_attribute():
    from bots import botslib
    err = botslib.BotsError('value %(v)s too long', {'v': 'x'})
    assert str(err) == 'value x too long'
    assert err.msg == 'value %(v)s too long'            # bots 3 attribute name
    with pytest.raises(botslib.BotsError):
        raise botslib.CommunicationOutError('x')


# ---------------------------------------------------------------- incoming: whitespace

def test_incoming_values_are_stripped_by_default(tmp_path):
    edi = parse(tmp_path, 'csv', 'ut_strip', 'HEA, Jansen ,  12.5 ,20200101 ,"   "\r\n')
    assert not edi.errorfatal and not edi.errorlist, edi.errorlist
    assert records(edi) == [{'BOTSID': 'HEA', 'NAME': 'Jansen', 'QTY': '12.5', 'DATE': '20200101'}]


def test_x12_edifact_tradacoms_default_to_stripping():
    from bots import grammar
    for cls in (grammar.csv, grammar.edifact, grammar.x12, grammar.tradacoms):
        assert cls.defaultsyntax['strip_value'] is True, cls.__name__


def test_strip_can_be_switched_off_but_numbers_stay_clean(tmp_path):
    edi = parse(tmp_path, 'csv', 'ut_nostrip', 'HEA, Jansen ,12.5 ,20200101,  7\r\n')
    assert not edi.errorfatal and not edi.errorlist, edi.errorlist
    rec = records(edi)[0]
    assert rec['NAME'] == ' Jansen '                      # text kept as received
    assert rec['QTY'] == '12.5'                           # not '12.50'
    assert rec['PRICE'] == '7'


# ---------------------------------------------------------------- outgoing: json

def test_json_one_message_is_an_object(botsenv):
    out = new_out('json', 'ut_orders')
    out.put({'BOTSID': 'order', 'nr': '1'})
    out.put({'BOTSID': 'order'}, {'BOTSID': 'line', 'item': 'a'})
    out.writeall()
    assert written(out).startswith(b'{')
    assert written_json(out) == {'order': {'nr': '1', 'line': [{'item': 'a'}]}}


def test_json_several_messages_are_a_list(botsenv):
    out = new_out('json', 'ut_orders')
    for nr in ('1', '2'):
        out.putloop({'BOTSID': 'order'}).put({'BOTSID': 'order', 'nr': nr})
    out.writeall()
    assert written_json(out) == [{'order': {'nr': '1'}}, {'order': {'nr': '2'}}]


def test_json_force_list(botsenv):
    out = new_out('json', 'ut_orders_list')
    out.put({'BOTSID': 'order', 'nr': '1'})
    out.writeall()
    assert written_json(out) == [{'order': {'nr': '1'}}]


def test_jsonnocheck_writes(botsenv):
    out = new_out('jsonnocheck', 'ut_free')
    out.put({'BOTSID': 'order', 'nr': '1'})
    out.put({'BOTSID': 'order'}, {'BOTSID': 'line', 'item': 'a'})
    out.writeall()
    assert written_json(out) == {'order': {'nr': '1', 'line': [{'item': 'a'}]}}


# ---------------------------------------------------------------- x12 envelope default

def test_x12_asks_for_acknowledgement_by_default():
    from bots import grammar
    assert grammar.x12.defaultsyntax['ISA14'] == '1'


def test_new_arguments_are_not_passed_to_an_exit_of_bots3():
    from bots import botslib

    class Script:
        @staticmethod
        def accept_incoming_attachment(channeldict, ta, charset, content, contenttype):
            return (channeldict, contenttype)

    class NewScript:
        @staticmethod
        def accept_incoming_attachment(channeldict, filename=None, **kwargs):
            return (filename, sorted(kwargs))

    argv = dict(channeldict=1, ta=2, charset=3, content=4, contenttype=5, content_disposition=6, filename=7)
    assert botslib.runscript(Script, 'script.py', 'accept_incoming_attachment', **argv) == (1, 5)
    assert botslib.runscript(NewScript, 'script.py', 'accept_incoming_attachment', **argv) == (
        7, ['charset', 'content', 'content_disposition', 'contenttype', 'ta'])
    # only for the arguments that are new: a wrong argument is still an error
    with pytest.raises(botslib.ScriptError):
        botslib.runscript(Script, 'script.py', 'accept_incoming_attachment', channeldict=1, unknown=2)


def test_bots_usersys_is_the_usersys_in_use(botsenv):
    import importlib
    from bots import botsglobal
    usersys = importlib.import_module(botsglobal.usersysimportpath)
    assert importlib.import_module('bots.usersys') is usersys
    import bots.usersys.grammars            # pylint: disable=import-outside-toplevel
    assert os.path.dirname(bots.usersys.grammars.__file__) == os.path.join(botsenv, 'usersys', 'grammars')


def test_make_index_called_as_in_bots3(botsenv, tmp_path):
    import json
    from bots import pluglib
    filename = str(tmp_path / 'index.json')
    cleaned_data = {'databaseconfiguration': True, 'umlists': False, 'databasetransactions': False}
    pluglib.make_index(cleaned_data, filename)
    with open(filename, encoding='utf8') as f:
        assert isinstance(json.load(f), (list, dict))

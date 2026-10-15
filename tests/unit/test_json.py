"""json: reading (empty content, lists of values, root of jsonnocheck) and writing (boolean, MAX 1 records)."""
import pytest

from helpers import new_out, parse, records, write_grammar, written_json

GRAMMAR = '''
    from bots.botsconfig import *
    syntax = {%s}
    structure = [{ID: 'order', MIN: 1, MAX: 99, LEVEL: [
        {ID: 'head', MIN: 0, MAX: 1},
        {ID: 'line', MIN: 0, MAX: 99},
    ]}]
    recorddefs = {
        'order': [['BOTSID', 'M', 20, 'A'], ['nr', 'C', 35, 'AN'], ['urgent', 'C', 5, 'B'], ['qty', 'C', 10, 'N']],
        'head': [['BOTSID', 'M', 20, 'A'], ['ref', 'C', 35, 'AN']],
        'line': [['BOTSID', 'M', 20, 'A'], ['item', 'C', 35, 'AN']],
    }
'''


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    write_grammar('json', 'ut_json', GRAMMAR % '')
    write_grammar('json', 'ut_json_object', GRAMMAR % "'max1_as_object': True")
    write_grammar('jsonnocheck', 'ut_free_in', "from bots.botsconfig import *\nsyntax = {}\n")
    write_grammar('jsonnocheck', 'ut_free_root', "from bots.botsconfig import *\nsyntax = {'defaultBOTSIDroot': 'msg'}\n")


def plain(record):
    """record without the number bots uses internally"""
    return dict((key, value) for key, value in record.items() if key != 'BOTSIDnr')


def order(out, **fields):
    out.put(dict({'BOTSID': 'order', 'nr': '1'}, **fields))
    out.put({'BOTSID': 'order'}, {'BOTSID': 'head', 'ref': 'R1'})
    for item in ('a', 'b'):
        line = out.putloop({'BOTSID': 'order'}, {'BOTSID': 'line'})
        line.put({'BOTSID': 'line', 'item': item})
    out.writeall()
    return written_json(out)


# ---------------------------------------------------------------- writing

def test_records_are_lists_as_in_bots3(botsenv):
    out = new_out('json', 'ut_json')
    assert order(out) == {'order': {'nr': '1', 'head': [{'ref': 'R1'}], 'line': [{'item': 'a'}, {'item': 'b'}]}}


def test_record_that_occurs_once_as_object_when_asked(botsenv):
    out = new_out('json', 'ut_json_object')
    assert order(out) == {'order': {'nr': '1', 'head': {'ref': 'R1'}, 'line': [{'item': 'a'}, {'item': 'b'}]}}


@pytest.mark.parametrize('given, expected', [(True, True), (False, False), ('true', True), ('0', False)])
def test_boolean_field(botsenv, given, expected):
    out = new_out('json', 'ut_json')
    assert order(out, urgent=given)['order']['urgent'] is expected


def test_boolean_field_with_another_value_is_an_error(botsenv):
    from bots.exceptions import MessageError
    out = new_out('json', 'ut_json')
    with pytest.raises(MessageError, match='F35'):
        order(out, urgent='maybe')


# ---------------------------------------------------------------- reading

@pytest.mark.parametrize('content', ['{}', '[]', '[{}]', '{"order": {}}'])
def test_no_usable_content(tmp_path, content):
    edi = parse(tmp_path, 'json', 'ut_json', content)
    text = ''.join(edi.errorlist)
    assert edi.errorfatal and '[J52]' in text and 'NoneType' not in text, text


def test_values_are_strings(tmp_path):
    edi = parse(tmp_path, 'json', 'ut_json', '{"order": {"nr": 12, "urgent": true, "qty": 3, "line": [{"item": 5}]}}')
    assert not edi.errorfatal and not edi.errorlist, edi.errorlist
    assert records(edi) == [{'BOTSID': 'order', 'nr': '12', 'urgent': 'True', 'qty': '3'},
                            {'BOTSID': 'line', 'item': '5'}]


def test_list_of_values_where_one_value_is_expected(tmp_path):
    edi = parse(tmp_path, 'json', 'ut_json', '{"order": {"nr": "1", "qty": [1, 2]}}')
    text = ''.join(edi.errorlist)
    assert '[J57]' in text and "has no attribute" not in text, text


def test_list_of_values_without_grammar(tmp_path):
    """jsonnocheck: values in a list are strings; objects in the same list are records"""
    edi = parse(tmp_path, 'jsonnocheck', 'ut_free_root', '{"nr": "1", "tags": ["a", 2, 3.5, {"deep": "x"}]}')
    assert not edi.errorfatal, edi.errorlist
    assert edi.root.record['tags'] == ['a', '2', '3.5']
    assert [plain(child.record) for child in edi.root.children] == [{'BOTSID': 'tags', 'deep': 'x'}]


def test_jsonnocheck_root_is_the_name_in_the_file_as_in_bots3(tmp_path):
    edi = parse(tmp_path, 'jsonnocheck', 'ut_free_in', '{"order": {"nr": "1", "line": [{"item": "a"}]}}')
    assert not edi.errorfatal, edi.errorlist
    assert plain(edi.root.record) == {'BOTSID': 'order', 'nr': '1'}
    assert edi.get({'BOTSID': 'order', 'nr': None}) == '1'
    assert edi.get({'BOTSID': 'order'}, {'BOTSID': 'line', 'item': None}) == 'a'


def test_jsonnocheck_root_as_set_in_grammar(tmp_path):
    edi = parse(tmp_path, 'jsonnocheck', 'ut_free_root', '{"order": {"nr": "1"}}')
    assert not edi.errorfatal, edi.errorlist
    assert edi.root.record['BOTSID'] == 'msg'
    assert edi.get({'BOTSID': 'msg'}, {'BOTSID': 'order', 'nr': None}) == '1'
    # no name in the file: the name of the grammar (or the default, ROOT)
    edi = parse(tmp_path, 'jsonnocheck', 'ut_free_in', '{"nr": "1", "ref": "x"}')
    assert plain(edi.root.record) == {'BOTSID': 'ROOT', 'nr': '1', 'ref': 'x'}

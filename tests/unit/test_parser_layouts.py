"""Layouts of standard definitions the reader has to handle.

- A record that has reached its MAX is looked for further on (nested LS...LE loops as in X12 217/218).
- Groups with the same header one after the other are told apart by the record after the header (as in X12 200,
  832); layouts that stay ambiguous are refused with a message that names both records.
- A composite with one component (EDIFACT ARR, C770 with 9424, repeated).

The grammars are written inline; the EDIFACT envelope comes from an official plugin of the regression tests.
"""
import os
import zipfile

import pytest

from helpers import new_out, parse, write_grammar, written

TESTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS = os.path.join(TESTS, 'regression', 'plugins', 'base')
EDIFACT_PLUGIN = os.path.join(PLUGINS, 'edifact2xml_orders-desadv-invoic_20130701.zip')

RECORDS = "{%s}" % ', '.join("'%s': [['BOTSID', 'M', 3, 'AN'], ['V', 'C', 10, 'AN']]" % rid for rid in (
    'HDR', 'LS', 'N1', 'LX', 'LE', 'NTE', 'REF', 'END', 'DTM', 'AAA', 'BBB', 'CCC'))
NESTED_LOOPS = '''
    from bots.botsconfig import *
    syntax = {'field_sep': ','}
    structure = [{ID: 'HDR', MIN: 1, MAX: 1, LEVEL: [
        {ID: 'LS', MIN: 0, MAX: 1, LEVEL: [
            {ID: 'N1', MIN: 1, MAX: 9, LEVEL: [
                {ID: 'LS', MIN: 0, MAX: 1, LEVEL: [
                    {ID: 'LX', MIN: 1, MAX: 9},
                    {ID: 'LE', MIN: 1, MAX: 1},
                ]},
            ]},
            {ID: 'LE', MIN: 1, MAX: 1},
        ]},
        {ID: 'DTM', MIN: 0, MAX: 2},
        {ID: 'END', MIN: 1, MAX: 1},
    ]}]
    recorddefs = %s
''' % RECORDS
LOOPS_IN_A_ROW = '''
    from bots.botsconfig import *
    syntax = {'field_sep': ','}
    structure = [{ID: 'HDR', MIN: 1, MAX: 1, LEVEL: [
        {ID: 'LS', MIN: 0, MAX: 1, LEVEL: [{ID: 'NTE', MIN: 1, MAX: 9}, {ID: 'LE', MIN: 1, MAX: 1}]},
        {ID: 'LS', MIN: 0, MAX: 1, LEVEL: [{ID: 'REF', MIN: 1, MAX: 9}, {ID: 'LE', MIN: 1, MAX: 1}]},
        {ID: 'END', MIN: 1, MAX: 1},
    ]}]
    recorddefs = %s
''' % RECORDS
BACK_COLLISION = '''
    from bots.botsconfig import *
    syntax = {'field_sep': ','}
    structure = [{ID: 'HDR', MIN: 1, MAX: 1, LEVEL: [
        {ID: 'AAA', MIN: 0, MAX: 9, LEVEL: [{ID: 'BBB', MIN: 0, MAX: 1}]},
        {ID: 'CCC', MIN: 0, MAX: 1},
        {ID: 'BBB', MIN: 0, MAX: 9},
        {ID: 'END', MIN: 1, MAX: 1},
    ]}]
    recorddefs = %s
''' % RECORDS
NESTING_COLLISION = '''
    from bots.botsconfig import *
    syntax = {'field_sep': ','}
    structure = [{ID: 'HDR', MIN: 1, MAX: 1, LEVEL: [
        {ID: 'AAA', MIN: 0, MAX: 9, LEVEL: [
            {ID: 'BBB', MIN: 0, MAX: 9, LEVEL: [{ID: 'AAA', MIN: 0, MAX: 1}]},
        ]},
        {ID: 'END', MIN: 1, MAX: 1},
    ]}]
    recorddefs = %s
''' % RECORDS
ARRAY = '''
    from bots.botsconfig import *
    syntax = {'version': '4'}
    structure = [{ID: 'UNH', MIN: 1, MAX: 1, LEVEL: [
        {ID: 'ARR', MIN: 1, MAX: 9},
        {ID: 'UNT', MIN: 1, MAX: 1},
    ]}]
    recorddefs = dict(
        UNH=[
            ['BOTSID', 'M', 3, 'AN'],
            ['0062', 'M', 14, 'AN'],
            ['S009', 'M', [['S009.0065', 'M', 6, 'AN'], ['S009.0052', 'M', 3, 'AN'], ['S009.0054', 'M', 3, 'AN'],
                           ['S009.0051', 'M', 2, 'AN'], ['S009.0057', 'C', 6, 'AN']]],
        ],
        UNT=[['BOTSID', 'M', 3, 'AN'], ['0074', 'M', 6, 'N'], ['0062', 'M', 14, 'AN']],
        ARR=[
        ['BOTSID', 'M', 3, 'AN'],
        ['C778', 'C', [['C778.7164', 'C', 35, 'AN'], ['C778.1050', 'C', 10, 'AN']]],
        ['C770', ('C', 9999), [['C770.9424', 'C', 512, 'AN']]],
        ['C999', 'C', [['C999.9999', 'C', 10, 'AN']]],
    ])
'''


def copy_plugin_grammars(plugin, editype, botsenv):
    target = os.path.join(botsenv, 'usersys', 'grammars', editype)
    with zipfile.ZipFile(plugin) as z:
        for name in z.namelist():
            if name.startswith('usersys/grammars/%s/' % editype) and name.endswith('.py') \
                    and not name.endswith('__init__.py'):
                with open(os.path.join(target, os.path.basename(name)), 'wb') as f:
                    f.write(z.read(name))


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    copy_plugin_grammars(EDIFACT_PLUGIN, 'edifact', botsenv)
    write_grammar('csv', 'ut_nested_loops', NESTED_LOOPS)
    write_grammar('csv', 'ut_loops_in_a_row', LOOPS_IN_A_ROW)
    write_grammar('csv', 'ut_back_collision', BACK_COLLISION)
    write_grammar('csv', 'ut_nesting_collision', NESTING_COLLISION)
    write_grammar('edifact', 'ARRAYSD99BUN', ARRAY)


def tree(edi, field):
    """(path of BOTSIDs, value of field) for every record of the parsed file, in file order."""
    found = []

    def walk(node, path):
        if node.record:
            path = path + [node.record['BOTSID']]
            found.append(('/'.join(path), node.record.get(field)))
        for child in node.children:
            walk(child, path)
    walk(edi.root, [])
    return found


def errors(edi):
    return ''.join(edi.errorlist) or ('fatal' if edi.errorfatal else '')


def refusal(editype, messagetype):
    from bots import grammar
    from bots.exceptions import GrammarError
    with pytest.raises(GrammarError) as exc:
        grammar.grammarread(editype, messagetype, typeofgrammarfile='grammars')
    return str(exc.value)


# ---------------------------------------------------------------- a record that has reached its MAX

def test_nested_loops_each_close_with_their_own_end(tmp_path):
    edi = parse(tmp_path, 'csv', 'ut_nested_loops',
                'HDR,1\r\nLS,A\r\nN1,x\r\nLS,B\r\nLX,1\r\nLE,B\r\nLE,A\r\nEND,1\r\n')
    assert not errors(edi), errors(edi)
    assert tree(edi, 'V') == [
        ('HDR', '1'), ('HDR/LS', 'A'), ('HDR/LS/N1', 'x'), ('HDR/LS/N1/LS', 'B'), ('HDR/LS/N1/LS/LX', '1'),
        ('HDR/LS/N1/LS/LE', 'B'), ('HDR/LS/LE', 'A'), ('HDR/END', '1')]


def test_a_single_loop_is_read_as_before(tmp_path):
    edi = parse(tmp_path, 'csv', 'ut_nested_loops', 'HDR,1\r\nLS,A\r\nN1,x\r\nN1,y\r\nLE,A\r\nEND,1\r\n')
    assert not errors(edi), errors(edi)
    assert tree(edi, 'V') == [('HDR', '1'), ('HDR/LS', 'A'), ('HDR/LS/N1', 'x'), ('HDR/LS/N1', 'y'),
                              ('HDR/LS/LE', 'A'), ('HDR/END', '1')]


def test_too_many_of_a_record_is_still_reported_as_too_many(tmp_path):
    """the record can go nowhere else: the message is the one of Bots 4 (occurs 3 times, max is 2)"""
    edi = parse(tmp_path, 'csv', 'ut_nested_loops', 'HDR,1\r\nDTM,1\r\nDTM,2\r\nDTM,3\r\nEND,1\r\n')
    assert 'occurs 3 times, max is 2' in errors(edi), errors(edi)


# ---------------------------------------------------------------- groups with the same header in a row

def test_the_record_after_the_header_chooses_between_groups_in_a_row(tmp_path):
    edi = parse(tmp_path, 'csv', 'ut_loops_in_a_row', 'HDR,1\r\nLS,B\r\nREF,r\r\nLE,B\r\nEND,1\r\n')
    assert not errors(edi), errors(edi)
    assert tree(edi, 'V') == [('HDR', '1'), ('HDR/LS', 'B'), ('HDR/LS/REF', 'r'), ('HDR/LS/LE', 'B'),
                              ('HDR/END', '1')]
    second = edi.root.children[0].children[0]
    assert second.record['BOTSIDnr'] == '2', 'the record is in the second LS group of the definition'


def test_groups_in_a_row_both_present(tmp_path):
    edi = parse(tmp_path, 'csv', 'ut_loops_in_a_row',
                'HDR,1\r\nLS,A\r\nNTE,n\r\nLE,A\r\nLS,B\r\nREF,r\r\nLE,B\r\nEND,1\r\n')
    assert not errors(edi), errors(edi)
    assert [child.record['BOTSIDnr'] for child in edi.root.children[0].children] == ['1', '2', '1']


def test_a_group_in_a_row_that_fits_neither_is_an_error(tmp_path):
    edi = parse(tmp_path, 'csv', 'ut_loops_in_a_row',
                'HDR,1\r\nLS,A\r\nNTE,n\r\nLE,A\r\nLS,B\r\nNTE,m\r\nLE,B\r\nEND,1\r\n')
    assert '[S50]' in errors(edi), errors(edi)


def test_back_collision_names_both_records():
    message = refusal('csv', 'ut_back_collision')
    assert 'back-collision detected at record "HDR-BBB"' in message
    assert '"HDR-AAA-BBB"' in message


def test_nesting_collision_names_both_records():
    message = refusal('csv', 'ut_nesting_collision')
    assert 'nesting collision detected at record "HDR-AAA-BBB-AAA"' in message
    assert '"HDR-AAA"' in message


# ---------------------------------------------------------------- a composite with one component

ARR_FILE = ("UNA:+.?*'UNB+UNOC:4+SENDER+RECEIVER+260101:1200+1'UNH+1+ARRAYS:D:99B:UN'"
            "ARR+1:2+A*B?*C*D+X'ARR++E'UNT+4+1'UNZ+1+1'")


def test_a_composite_with_one_component_is_read(tmp_path):
    edi = parse(tmp_path, 'edifact', 'edifact', ARR_FILE)
    assert not errors(edi), errors(edi)
    message = next(iter(edi.nextmessage()))
    arrays = [node.record for node in message.getloop({'BOTSID': 'UNH'}, {'BOTSID': 'ARR'})]
    assert arrays[0]['C770'] == [{'C770.9424': 'A'}, {'C770.9424': 'B*C'}, {'C770.9424': 'D'}]
    assert arrays[0]['C999.9999'] == 'X'
    assert arrays[1]['C770'] == [{'C770.9424': 'E'}]


def test_a_composite_with_one_component_is_written():
    out = new_out('edifact', 'ARRAYSD99BUN')
    out.put({'BOTSID': 'UNH', '0062': '1', 'S009.0065': 'ARRAYS', 'S009.0052': 'D', 'S009.0054': '99B',
             'S009.0051': 'UN'})
    arr = out.putloop({'BOTSID': 'UNH'}, {'BOTSID': 'ARR'})
    arr.put({'BOTSID': 'ARR', 'C778.7164': '1', 'C778.1050': '2', 'C999.9999': 'X'})
    arr.record['C770'] = [{'C770.9424': 'A'}, {'C770.9424': 'B*C'}]
    out.put({'BOTSID': 'UNH'}, {'BOTSID': 'UNT', '0074': '3', '0062': '1'})
    out.writeall()
    assert b"ARR+1:2+A*B?*C+X'" in written(out), written(out)

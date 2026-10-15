"""Parser and node-tree details: edifact groups, fixed records without BOTSID, csv options, sort, putraw."""
import decimal
import os
import zipfile

import pytest

from helpers import new_out, parse, records, write_grammar

PLUGIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regression', 'plugins', 'base',
                      'edifact2xml_orders-desadv-invoic_20130701.zip')

FIXED_NOBOTSID = '''
    from bots.botsconfig import *
    syntax = {'noBOTSID': True, 'checkfixedrecordtooshort': True, 'checkfixedrecordtoolong': True}
    structure = [{ID: 'LIN', MIN: 1, MAX: 9999}]
    recorddefs = {'LIN': [['BOTSID', 'M', 3, 'A'], ['ART', 'C', 5, 'AN'], ['QTY', 'C', 4, 'N']]}
'''
CSV_SKIP = '''
    from bots.botsconfig import *
    syntax = {'field_sep': ',', 'skip_firstline': True}
    structure = [{ID: 'HEA', MIN: 0, MAX: 9999}]
    recorddefs = {'HEA': [['BOTSID', 'M', 3, 'A'], ['NAME', 'C', 35, 'AN']]}
'''
XML_SORT = '''
    from bots.botsconfig import *
    structure = [{ID: 'order', MIN: 1, MAX: 1, LEVEL: [{ID: 'line', MIN: 0, MAX: 9999}]}]
    recorddefs = {
        'order': [['BOTSID', 'M', 20, 'A'], ['nr', 'C', 35, 'AN']],
        'line': [['BOTSID', 'M', 20, 'A'], ['item', 'C', 35, 'AN'], ['qty', 'C', 16.3, 'R']],
    }
'''


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    write_grammar('fixed', 'ut_nobotsid', FIXED_NOBOTSID)
    write_grammar('csv', 'ut_skip', CSV_SKIP)
    write_grammar('xml', 'ut_sort', XML_SORT)
    # the edifact grammars of an official plugin (already ported to python 3)
    target = os.path.join(botsenv, 'usersys', 'grammars', 'edifact')
    with zipfile.ZipFile(PLUGIN) as z:
        for name in z.namelist():
            if name.startswith('usersys/grammars/edifact/') and name.endswith('.py') and not name.endswith('__init__.py'):
                with open(os.path.join(target, os.path.basename(name)), 'wb') as f:
                    f.write(z.read(name))


# ---------------------------------------------------------------- parser

def test_fixed_record_length_without_botsid(tmp_path):
    """records of ART(5)+QTY(4) = 9 positions; the BOTSID is not in the file"""
    edi = parse(tmp_path, 'fixed', 'ut_nobotsid', 'AAAAA0012\r\nBBBBB0003\r\n')
    assert not edi.errorfatal and not edi.errorlist, edi.errorfatal or edi.errorlist
    assert records(edi) == [{'BOTSID': 'LIN', 'ART': 'AAAAA', 'QTY': '12'}, {'BOTSID': 'LIN', 'ART': 'BBBBB', 'QTY': '3'}]
    short = parse(tmp_path, 'fixed', 'ut_nobotsid', 'AAAAA001\r\n')
    assert short.errorfatal and '[S52]' in ''.join(short.errorlist) and 'defined is 9 pos' in ''.join(short.errorlist)


def test_csv_skip_firstline_on_empty_file(tmp_path):
    edi = parse(tmp_path, 'csv', 'ut_skip', '')
    assert 'list assignment index out of range' not in (edi.errorfatal or '')
    edi = parse(tmp_path, 'csv', 'ut_skip', 'header,line\r\nHEA,x\r\n')
    assert records(edi) == [{'BOTSID': 'HEA', 'NAME': 'x'}]


ORDER = ("UNH+%s+ORDERS:D:96A:UN:EAN008'BGM+220+PO%s+9'DTM+137:20260101:102'NAD+BY+8712345678920::9'"
         "LIN+1++8712345000011:EN'QTY+21:5'UNS+S'UNT+8+%s'")


def test_edifact_interchange_with_groups(tmp_path):
    """UNB-UNG-UNH (functional groups): messages are split with nextmessage2"""
    content = ("UNB+UNOA:2+SENDER:14+RECEIVER:14+260101:1200+1'UNG+ORDERS+SENDER+RECEIVER+260101:1200+1+UN+D:96A:EAN008'"
               + ORDER % ('1', '1', '1') + ORDER % ('2', '2', '2') + "UNE+2+1'UNZ+1+1'")
    edi = parse(tmp_path, 'edifact', 'edifact', content)
    assert not edi.errorfatal, edi.errorfatal
    messages = list(edi.nextmessage())
    assert len(messages) == 2
    assert [m.get({'BOTSID': 'UNH'}, {'BOTSID': 'BGM', '1004': None}) for m in messages] == ['PO1', 'PO2']
    assert messages[0].ta_info['frompartner'] == 'SENDER'


def test_edifact_interchange_without_groups(tmp_path):
    content = "UNB+UNOA:2+SENDER:14+RECEIVER:14+260101:1200+1'" + ORDER % ('1', '1', '1') + "UNZ+1+1'"
    edi = parse(tmp_path, 'edifact', 'edifact', content)
    assert not edi.errorfatal, edi.errorfatal
    assert len(list(edi.nextmessage())) == 1


# ---------------------------------------------------------------- node tree

def build(items):
    out = new_out('xml', 'ut_sort')
    out.put({'BOTSID': 'order', 'nr': '1'})
    for item, qty in items:
        line = out.putloop({'BOTSID': 'order'}, {'BOTSID': 'line'})
        if item is not None:
            line.put({'BOTSID': 'line', 'item': item})
        if qty is not None:
            line.put({'BOTSID': 'line', 'qty': qty})
    return out


def order_of(out, field='item'):
    return [child.record.get(field) for child in out.root.children]


def test_sort_as_in_bots3(botsenv):
    out = build([('B', None), ('A', None), (None, '9'), ('1', None)])
    out.sort({'BOTSID': 'order'}, {'BOTSID': 'line', 'item': None})
    assert order_of(out) == [None, '1', 'A', 'B']          # records without the key come first


def test_sort_keywords_on_message(botsenv):
    out = build([('B', '10'), ('A', '2'), ('C', '0'), ('D', None)])
    out.sort(sortfrom=({'BOTSID': 'order'},), compare=({'BOTSID': 'line', 'qty': None},), sort_decimal=True)
    assert order_of(out) == ['C', 'D', 'A', 'B']           # numeric: 0, (missing = 0), 2, 10
    out.sort({'BOTSID': 'order'}, {'BOTSID': 'line', 'item': None}, reverse=True)
    assert order_of(out) == ['D', 'C', 'B', 'A']
    out = build([('B', None), (None, '1'), ('A', None)])
    out.sort({'BOTSID': 'order'}, {'BOTSID': 'line', 'item': None}, sort_if_none='zzz')
    assert order_of(out) == ['A', 'B', None]


def test_getdecimal_of_non_numeric_value_is_zero(botsenv):
    out = build([('abc', None)])
    line = out.root.children[0]
    assert line.getdecimal({'BOTSID': 'line', 'item': None}) == decimal.Decimal('0')
    assert line.getdecimal({'BOTSID': 'line', 'qty': None}) == decimal.Decimal('0')


def test_putraw(botsenv):
    out = new_out('xml', 'ut_sort')
    assert out.putraw({'BOTSID': 'order', 'nr': '7'}) is True
    assert out.root.record['nr'] == '7'
    assert out.putraw({'BOTSID': 'order', 'nr': None}) is False

"""Mapping functions and names of bots 3; texts of errors; small checks in the parser."""
import os
import subprocess
import sys
import zipfile

import pytest

from helpers import parse, write_grammar

PLUGIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regression', 'plugins', 'base',
                      'edifact2xml_orders-desadv-invoic_20130701.zip')

FIXED = '''
    from bots.botsconfig import *
    syntax = {'charset': 'us-ascii'}
    structure = [{ID: 'HEA', MIN: 1, MAX: 1, LEVEL: [{ID: 'LIN', MIN: 1, MAX: 99}]}]
    recorddefs = {
        'HEA': [['BOTSID', 'M', 3, 'A'], ['NR', 'C', 5, 'AN']],
        'LIN': [['BOTSID', 'M', 3, 'A'], ['QTY', 'C', 6, 'N'], ['PRICE', 'C', 8.2, 'R'], ['CENTS', 'C', 6.2, 'I']],
    }
'''
OLD_KEYS = '''
    from bots.botsconfig import *
    syntax = {'no_results_if_any_error_in_translation_edifile': True, 'allow_spaces_between_records': False}
    structure = [{ID: 'HEA', MIN: 1, MAX: 1}]
    recorddefs = {'HEA': [['BOTSID', 'M', 3, 'A'], ['NR', 'C', 5, 'AN']]}
'''
GRAMMAR = '''
    from bots.botsconfig import *
    structure = [{ID: 'HEA', MIN: 1, MAX: 1}]
    recorddefs = {'HEA': [['BOTSID', 'M', 3, 'A'], %s]}
'''


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    write_grammar('fixed', 'ut_numbers', FIXED)
    write_grammar('fixed', 'ut_oldkeys', OLD_KEYS)
    write_grammar('fixed', 'ut_decimals', GRAMMAR % "['PRICE', 'C', 2.5, 'R']")
    write_grammar('fixed', 'ut_format', GRAMMAR % "['PRICE', 'C', 5, 'ZZ']")
    target = os.path.join(botsenv, 'usersys', 'grammars', 'edifact')
    with zipfile.ZipFile(PLUGIN) as z:
        for name in z.namelist():
            if name.startswith('usersys/grammars/edifact/') and name.endswith('.py') and not name.endswith('__init__.py'):
                with open(os.path.join(target, os.path.basename(name)), 'wb') as f:
                    f.write(z.read(name))


# ---------------------------------------------------------------- names and functions of bots 3

def test_constants_via_transform(botsenv):
    from bots import botsconfig, transform
    for name in ('TRANSLATED', 'FILEIN', 'EXTERNOUT', 'ID', 'MIN', 'MAX', 'OK', 'ERROR'):
        assert getattr(transform, name) == getattr(botsconfig, name), name


def test_partnerlookup_field_without_value_is_not_found(botsenv):
    from bots import models, transform
    from bots.exceptions import CodeConversionError
    models.partner(idpartner='UTLOOK', active=True, name='lookup', attr1='', attr2='GLN123').save()
    try:
        assert transform.partnerlookup('UTLOOK', 'attr2') == 'GLN123'
        assert transform.partnerlookup('GLN123', 'idpartner', 'attr2') == 'UTLOOK'
        # the name of the 3rd parameter in bots 3
        assert transform.partnerlookup('GLN123', 'idpartner', field_where_value_is_searched='attr2') == 'UTLOOK'
        # partner is there, field is empty: as a partner that is not there
        assert transform.partnerlookup('UTLOOK', 'attr1', safe=True) == 'UTLOOK'
        assert transform.partnerlookup('UTLOOK', 'attr1', safe=None) is None
        with pytest.raises(CodeConversionError):
            transform.partnerlookup('UTLOOK', 'attr1')
        with pytest.raises(CodeConversionError):
            transform.partnerlookup('NOTTHERE', 'attr2')
    finally:
        models.partner.objects.filter(idpartner='UTLOOK').delete()


def test_envelope_of_a_message_by_its_bots3_name(tmp_path):
    content = ("UNB+UNOA:2+SENDER:14+RECEIVER:14+260101:1200+1'"
               "UNH+1+ORDERS:D:96A:UN:EAN008'BGM+220+PO1+9'DTM+137:20260101:102'NAD+BY+8712345678920::9'"
               "LIN+1++8712345000011:EN'QTY+21:5'UNS+S'UNT+8+1'UNZ+1+1'")
    edi = parse(tmp_path, 'edifact', 'edifact', content)
    assert not edi.errorfatal, edi.errorlist
    message = list(edi.nextmessage())[0]
    assert message.envelope is message.envelope_content and message.envelope


def test_syntax_parameters_with_their_bots3_names(botsenv):
    from bots import grammar
    syntax = grammar.grammarread('fixed', 'ut_oldkeys', typeofgrammarfile='grammars').syntax
    assert syntax['KillWholeFile'] is True and syntax['strict_syntax_check'] is True


# ---------------------------------------------------------------- texts of errors

def test_error_of_a_file_is_the_error_itself(tmp_path):
    """not: the python errors that led to it"""
    edi = parse(tmp_path, 'fixed', 'ut_numbers', 'HEA00001\r\n')              # mandatory LIN is missing
    text = ''.join(edi.errorlist)
    assert edi.errorfatal and '[S5' in text, text
    for noise in ('Traceback', 'direct cause', 'During handling', 'File "'):
        assert noise not in text, text
    edi = parse(tmp_path, 'fixed', 'ut_nosuchgrammar', 'HEA00001\r\n')
    text = ''.join(edi.errorlist)
    assert 'ut_nosuchgrammar' in text and 'Traceback' not in text and 'direct cause' not in text, text


def test_strict_check_messages_are_complete(tmp_path):
    for content, code in (("UNB+UNOA:2+S:14+R:14+260101:1200+1'  UNZ+0+1'", '[A67]'),
                          ("UNB+UNOA:2+S:14+R:14+260101:1200+1''UNZ+0+1'", '[A69]')):
        edi = parse(tmp_path, 'edifact', 'edifact', content, strict_syntax_check=True)
        text = ''.join(edi.errorlist)
        assert code in text and 'Line 1, position' in text and '%(' not in text and 'position ,' not in text, text


@pytest.mark.parametrize('name, expected', [
    ('ut_decimals', 'field length "2" has to be greater that nr of decimals "5"'),
    ('ut_format', 'format "ZZ" has to be one of "A, AN,'),
])
def test_grammar_error_texts(botsenv, name, expected):
    from bots import grammar
    from bots.exceptions import GrammarError
    with pytest.raises(GrammarError) as info:
        grammar.grammarread('fixed', name, typeofgrammarfile='grammars')
    assert expected in str(info.value) and 'dict_keys' not in str(info.value), str(info.value)


def test_grammarcheck_reports_a_grammar_that_can_not_be_imported(botsenv):
    write_grammar('fixed', 'ut_broken', 'import this_module_does_not_exist\n')
    script = "import sys; sys.argv[0] = 'bots-grammarcheck'; from bots.grammarcheck import start; start()"
    done = subprocess.run([sys.executable, '-c', script, 'fixed', 'ut_broken'], capture_output=True, text=True,
                          env=dict(os.environ, BOTS_CONFIG_DIR=os.path.join(botsenv, 'config')))
    output = done.stdout + done.stderr
    assert done.returncode == 1 and 'Found error in grammar' in done.stdout, output
    assert 'this_module_does_not_exist' in output and 'Traceback' not in output, output


# ---------------------------------------------------------------- numbers

def test_underscore_is_not_part_of_a_number(tmp_path):
    good = parse(tmp_path, 'fixed', 'ut_numbers', 'HEA00001\r\nLIN00001000012.5000150\r\n')
    assert not good.errorfatal and not good.errorlist, good.errorlist
    for line in ('LIN001_0000012.5000150', 'LIN0000100001_.5000150', 'LIN00001000012.50001_0'):
        edi = parse(tmp_path, 'fixed', 'ut_numbers', 'HEA00001\r\n' + line + '\r\n')
        assert edi.errorlist or edi.errorfatal, line
        assert 'numerical' in ''.join(edi.errorlist) or '[F' in ''.join(edi.errorlist), ''.join(edi.errorlist)

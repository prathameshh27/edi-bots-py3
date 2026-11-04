"""The envelope of a 997 or CONTRL bots makes for an interchange received.

bots.ini [settings] acknowledgement_envelope_as_received = True: the acknowledgement is written and enveloped with
the syntax of the interchange it answers (x12: ISA12, ISA11 before 00403, the separators; edifact: syntax identifier
and version, separators, UNA), unless the partner syntax sets them. Not set: the envelope grammar's values (bots 3).
"""
import os
import sys
import zipfile

import pytest

from helpers import parse, write_grammar

PLUGINS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regression', 'plugins', 'base')
X12_PLUGIN = os.path.join(PLUGINS, 'x12toxml_retailer_version_850-856-810-997_20130807.zip')
EDIFACT_PLUGIN = os.path.join(PLUGINS, 'edifact2xml_orders-desadv-invoic_20130701.zip')
OPTION = 'acknowledgement_envelope_as_received'

# the CONTRL bots writes itself (inmessage.edifact.handleconfirm); only the segments it writes
CONTRL = '''
    from bots.botsconfig import *
    structure = [{ID: 'UNH', MIN: 1, MAX: 1, LEVEL: [
        {ID: 'UCI', MIN: 1, MAX: 1},
        {ID: 'UCM', MIN: 0, MAX: 999999},
        {ID: 'UNT', MIN: 1, MAX: 1},
    ]}]
    def _S009():
        return ['S009', 'M', [['S009.0065', 'M', 6, 'AN'], ['S009.0052', 'M', 3, 'AN'], ['S009.0054', 'M', 3, 'AN'],
                              ['S009.0051', 'M', 2, 'AN'], ['S009.0057', 'C', 6, 'AN']]]
    recorddefs = {
        'UNH': [['BOTSID', 'M', 3, 'AN'], ['0062', 'M', 14, 'AN'], _S009()],
        'UCI': [['BOTSID', 'M', 3, 'AN'], ['0020', 'M', 14, 'AN'],
                ['S002', 'M', [['S002.0004', 'M', 35, 'AN'], ['S002.0007', 'C', 4, 'AN'],
                               ['S002.0008', 'C', 35, 'AN'], ['S002.0042', 'C', 35, 'AN']]],
                ['S003', 'M', [['S003.0010', 'M', 35, 'AN'], ['S003.0007', 'C', 4, 'AN'],
                               ['S003.0014', 'C', 35, 'AN'], ['S003.0046', 'C', 35, 'AN']]],
                ['0083', 'M', 3, 'AN']],
        'UCM': [['BOTSID', 'M', 3, 'AN'], ['0062', 'M', 14, 'AN'], _S009(), ['0083', 'M', 3, 'AN']],
        'UNT': [['BOTSID', 'M', 3, 'AN'], ['0074', 'M', 6, 'N'], ['0062', 'M', 14, 'AN']],
    }
'''

INVOICE = ("ISA*00*          *00*          *01*0011223456     *01*999999999      *130123*0123*^*00403*000000001*1*P*>~"
           "GS*IN*0011223456*999999999*20130123*0123*1*X*004010~ST*810*0063~BIG*20070929*95018017**ordernumber***DR~"
           "N1*SE*UNIVERSAL WIDGETS~IT1*001*4*EA*330**VN*X357-W2***BP*525~TDS*1234579~CTT*1~SE*6*0063~GE*1*1~IEA*1*000000001~")
ORDER = ("UNH+1+ORDERS:D:96A:UN:EAN008'BGM+220+PO1+9'DTM+137:20260101:102'NAD+BY+8712345678920::9'"
         "LIN+1++8712345000011:EN'QTY+21:5'UNS+S'UNT+8+1'")


def copy_grammars(botsenv, plugin, editype):
    target = os.path.join(botsenv, 'usersys', 'grammars', editype)
    with zipfile.ZipFile(plugin) as z:
        for name in z.namelist():
            if name.startswith(f'usersys/grammars/{editype}/') and name.endswith('.py') \
                    and not name.endswith('__init__.py'):
                with open(os.path.join(target, os.path.basename(name)), 'wb') as f:
                    f.write(z.read(name))


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    copy_grammars(botsenv, X12_PLUGIN, 'x12')
    copy_grammars(botsenv, EDIFACT_PLUGIN, 'edifact')
    write_grammar('edifact', 'CONTRL22UNEAN002', CONTRL)


@pytest.fixture
def option(botsenv):
    from bots import botsglobal
    botsglobal.ini.set('settings', OPTION, 'True')
    yield
    botsglobal.ini.remove_option('settings', OPTION)


@pytest.fixture
def partner_syntax(botsenv):
    """write usersys/partners/<editype>/<partner>.py; removed afterwards"""
    from bots import botsglobal
    written = []

    def write(editype, partner, text):
        write_grammar(editype, partner, text, kind='partners')
        written.append((editype, partner))
    yield write
    for editype, partner in written:
        os.remove(os.path.join(botsglobal.ini.get('directories', 'usersysabs'), 'partners', editype, partner + '.py'))
        sys.modules.pop(f'{botsglobal.usersysimportpath}.partners.{editype}.{partner}', None)


def acknowledge(tmp_path, monkeypatch, editype, content):
    """parse content, make its acknowledgement and envelope it; returns (the enveloped file, rsrv5 of the
    acknowledgement)"""
    from bots import botsglobal, botslib, envelope
    from bots.botsconfig import MERGED, OK, PARSED, TRANSLATED
    confirmtype = 'send-x12-997' if editype == 'x12' else 'send-edifact-CONTRL'
    monkeypatch.setattr(botsglobal, 'confirmrules', [dict(
        confirmtype=confirmtype, ruletype='all', negativerule=False, idroute='', idchannel=None,
        frompartner=None, topartner=None, messagetype='', editype='')])
    start = max([row['idta'] for row in botslib.query('SELECT idta FROM ta')] or [0])
    edi = parse(tmp_path, editype, editype, content, idroute='utack', fromchannel='utack_in')
    assert not edi.errorfatal, edi.errorlist
    ta_fromfile = botslib.NewTransaction(status=PARSED, statust=OK, idroute='utack')
    edi.handleconfirm(ta_fromfile, {'idroute': 'utack'}, error=False)
    [made] = list(botslib.query('SELECT rsrv5 FROM ta WHERE idta>%(start)s AND status=%(status)s',
                                {'start': start, 'status': TRANSLATED}))
    envelope.mergemessages(TRANSLATED, MERGED, 'utack', rootidta=start)
    [row] = list(botslib.query('SELECT filename, statust, errortext FROM ta WHERE idta>%(start)s AND status=%(status)s',
                               {'start': start, 'status': MERGED}))
    assert row['statust'] == OK, row['errortext']
    with open(botslib.abspathdata(row['filename']), 'rb') as f:
        return f.read().decode('latin-1'), made['rsrv5']


def isa(text):
    """the ISA elements (ISA16 last, from its fixed position) and the segment terminator"""
    start = text.lstrip()
    return start[:106].split(start[3])[:16] + [start[104]], start[105]


def x12(version='00403', isa11='^'):
    return INVOICE.replace('*^*00403*', f'*{isa11}*{version}*')


# ---------------------------------------------------------------- x12

def test_997_without_the_option_is_enveloped_with_the_envelope_grammar(tmp_path, monkeypatch):
    """as bots 3: the version of the envelope grammar ('only for sending'), also for a 00401 interchange"""
    text, rsrv5 = acknowledge(tmp_path, monkeypatch, 'x12', x12('00401', 'U'))
    fields, term = isa(text)
    assert (fields[11], fields[12], fields[16], term) == ('^', '00403', '>', '~'), text
    assert 'ST*997*' in text and not rsrv5


def test_997_for_a_00401_interchange_is_00401_with_isa11(tmp_path, monkeypatch, option):
    text, _rsrv5 = acknowledge(tmp_path, monkeypatch, 'x12', x12('00401', 'U'))
    fields, _term = isa(text)
    assert (fields[11], fields[12]) == ('U', '00401'), text


def test_997_keeps_the_separators_of_a_00501_interchange(tmp_path, monkeypatch, option):
    """in its envelope and in its segments: | for elements, ! for repetitions, : within an element"""
    received = x12('00501', '!').replace('*>~', '*:~').replace('*', '|')
    text, _rsrv5 = acknowledge(tmp_path, monkeypatch, 'x12', received)
    fields, term = isa(text)
    assert (text.lstrip()[3], fields[11], fields[12], fields[16], term) == ('|', '!', '00501', ':', '~'), text
    assert 'ST|997|' in text and 'GS|FA|' in text and '*' not in text, text


def test_997_for_segments_that_end_in_a_line_break_has_bots_separators(tmp_path, monkeypatch, option):
    """bots writes a line break after each segment: the received separators are not taken over, the version is"""
    received = x12('00401', 'U').replace('~', '\n').replace('*', '|')
    text, _rsrv5 = acknowledge(tmp_path, monkeypatch, 'x12', received)
    fields, term = isa(text)
    assert (text.lstrip()[3], fields[11], fields[12], fields[16], term) == ('*', 'U', '00401', '>', '~'), text
    assert '\n\r\n' not in text and 'ST*997*' in text, text


def test_the_partner_syntax_wins_over_the_received_envelope(tmp_path, monkeypatch, option, partner_syntax):
    partner_syntax('x12', 'UTOWNSYNTAX', "syntax = {'version': '00403', 'field_sep': '+'}\n")
    received = x12('00401', 'U').replace('0011223456*', 'UTOWNSYNTAX*')
    text, _rsrv5 = acknowledge(tmp_path, monkeypatch, 'x12', received)
    fields, _term = isa(text)
    assert (text.lstrip()[3], fields[11], fields[12]) == ('+', '^', '00403'), text
    assert 'ST+997+' in text, text


# ---------------------------------------------------------------- edifact

def edifact(syntax, una=''):
    return f"{una}UNB+{syntax}+SENDER:14+RECEIVER:14+260101:1200+51'{ORDER}UNZ+1+51'"


def test_contrl_without_the_option_is_enveloped_with_the_envelope_grammar(tmp_path, monkeypatch):
    text, rsrv5 = acknowledge(tmp_path, monkeypatch, 'edifact', edifact('UNOA:2', "UNA:+.? '"))
    assert text.startswith("UNA:+.? '") and 'UNB+UNOC:3+' in text, text      # grammar edifact.py: UNOC, 3
    assert not rsrv5


@pytest.mark.parametrize('syntax, una', [('UNOA:2', "UNA:+.? '"), ('UNOC:3', ''), ('UNOA:4', '')])
def test_contrl_has_the_syntax_identifier_and_version_received(tmp_path, monkeypatch, option, syntax, una):
    text, _rsrv5 = acknowledge(tmp_path, monkeypatch, 'edifact', edifact(syntax, una))
    assert text[text.index('UNB+'):].startswith(f'UNB+{syntax}+'), text
    assert "UCI+51+SENDER:14+RECEIVER:14+7'" in text, text
    assert text.startswith('UNA') == (syntax != 'UNOA:4'), text      # UNOC: always a UNA, as bots writes


def test_contrl_keeps_the_separators_of_the_una(tmp_path, monkeypatch, option):
    received = edifact('UNOC:3', "UNA|#.? !").replace("'", '!').replace('+', '#').replace(':', '|')
    text, _rsrv5 = acknowledge(tmp_path, monkeypatch, 'edifact', received)
    assert text.startswith('UNA|#.? !') and 'UNB#UNOC|3#' in text and 'UCI#51#SENDER|14#RECEIVER|14#7!' in text, text

"""Enveloping: x12 GS04, IDmode, interchange counters, merging of messages with different envelope data."""
import json
import os
import zipfile

import pytest

from helpers import write_grammar

PLUGINS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regression', 'plugins', 'base')
X12_PLUGIN = os.path.join(PLUGINS, 'x12toxml_retailer_version_850-856-810-997_20130807.zip')
MESSAGE = "ST*850*0001~BEG*00*SA*PO1**20260101~SE*3*0001~\n"

IDMODE_GRAMMAR = '''
    import importlib
    _base = importlib.import_module('.850004010', __package__)
    structure = _base.structure
    recorddefs = _base.recorddefs
    syntax = {'IDmode': '%s'}
'''


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    target = os.path.join(botsenv, 'usersys', 'grammars', 'x12')
    with zipfile.ZipFile(X12_PLUGIN) as z:
        for name in z.namelist():
            if name.startswith('usersys/grammars/x12/') and name.endswith('.py') and not name.endswith('__init__.py'):
                with open(os.path.join(target, os.path.basename(name)), 'wb') as f:
                    f.write(z.read(name))
    write_grammar('x12', '850004010IDM', IDMODE_GRAMMAR % 'ISA_qualifier_GS')
    write_grammar('x12', '850004010IDQ', IDMODE_GRAMMAR % 'ISA_qualifier')
    write_grammar('x12', '850004010NOTA1', IDMODE_GRAMMAR.replace("'IDmode': '%s'", "'ISA14': '0'"))


_names = iter(range(5000, 9999))


def datafile(content=MESSAGE):
    from bots import botslib
    name = str(next(_names))
    with botslib.opendata(name, 'w', 'us-ascii') as f:
        f.write(content)
    return name


def read(name):
    from bots import botslib
    with open(botslib.abspathdata(name), 'rb') as f:
        return f.read().decode('ascii')


def segments(content):
    """{'ISA': [fields], 'GS': [fields], ...} of the first interchange"""
    found = {}
    for segment in content.replace('\r', '').replace('\n', '').split('~'):
        fields = segment.split('*')
        found.setdefault(fields[0], fields)
    return found


def x12_envelope(frompartner='SENDER', topartner='RECEIVER', messagetype='850004010', mapped=None):
    """envelope one message; returns (ta_info, segments of the result)"""
    from bots import envelope
    ta_info = dict(editype='x12', messagetype=messagetype, envelope='x12', frompartner=frompartner,
                   topartner=topartner, testindicator='', charset='us-ascii', nrmessages=1, idroute='ut',
                   filename=str(next(_names)), rsrv3='',
                   rsrv5=json.dumps({'envelope_content': mapped}) if mapped else '')
    envelope.envelope(ta_info, [datafile()])
    return ta_info, segments(read(ta_info['filename']))


# ---------------------------------------------------------------- GS04

def test_gs04_length_depends_on_version(botsenv):
    _ta, seg = x12_envelope()
    assert len(seg['GS'][4]) == 8 and seg['GS'][8] == '004010'
    _ta, seg = x12_envelope(mapped=[{}, {'GS08': '003020'}, {}, {}])
    assert len(seg['GS'][4]) == 6 and seg['GS'][8] == '003020'


def test_gs04_from_mapping_is_used_for_every_version(botsenv):
    _ta, seg = x12_envelope(mapped=[{}, {'GS04': '19991231'}, {}, {}])
    assert seg['GS'][4] == '19991231'
    _ta, seg = x12_envelope(mapped=[{}, {'GS04': '991231', 'GS08': '003020'}, {}, {}])
    assert seg['GS'][4] == '991231'


def test_isa14_is_what_mapping_or_syntax_say_also_with_a_confirmrule(botsenv, monkeypatch):
    """as bots 3: a confirmrule 'ask-x12-997' (here: for the route) does not set ISA14"""
    from bots import botsglobal
    rule = dict(confirmtype='ask-x12-997', ruletype='route', negativerule=False, idroute='ut', idchannel=None,
                frompartner=None, topartner=None, messagetype='', editype='')
    for rules in ([], [rule]):
        monkeypatch.setattr(botsglobal, 'confirmrules', rules)
        assert x12_envelope()[1]['ISA'][14] == '1'                                  # default of x12
        assert x12_envelope(messagetype='850004010NOTA1')[1]['ISA'][14] == '0'      # syntax of the grammar
        assert x12_envelope(mapped=[{'ISA14': '0'}, {}, {}, {}])[1]['ISA'][14] == '0'
        assert x12_envelope(messagetype='850004010NOTA1', mapped=[{'ISA14': '1'}, {}, {}, {}])[1]['ISA'][14] == '1'


def test_997_made_by_bots_is_004010_unless_asked_otherwise(botsenv):
    """as bots 3: always grammar 997004010, also when a 997 grammar for the received version exists"""
    from bots import botsglobal, inmessage
    write_grammar('x12', '997004060', IDMODE_GRAMMAR.replace('.850004010', '.997004010') % 'ISA')
    for version in ('004060', '004010', '004010VICS', '005010X222A1', None):
        assert inmessage.x12_997_messagetype(version) == '997004010'
    botsglobal.ini.set('settings', 'x12_997_version_as_received', 'True')
    try:
        assert inmessage.x12_997_messagetype('004060') == '997004060'
        assert inmessage.x12_997_messagetype('004060XYZ') == '997004060'       # implementation suffix
        assert inmessage.x12_997_messagetype('005010X222A1') == '997004010'    # no grammar for 005010
        assert inmessage.x12_997_messagetype(None) == '997004010'
    finally:
        botsglobal.ini.remove_option('settings', 'x12_997_version_as_received')


# ---------------------------------------------------------------- reference, IDmode

def test_reference_is_a_string_and_counts_per_sender(botsenv):
    ta1, seg1 = x12_envelope(frompartner='REFSENDER')
    ta2, seg2 = x12_envelope(frompartner='REFSENDER', topartner='OTHER')
    assert isinstance(ta1['reference'], str)
    assert int(ta2['reference']) == int(ta1['reference']) + 1
    assert int(seg1['ISA'][13]) == int(ta1['reference']) == int(seg1['GS'][6]) == int(seg1['IEA'][2])
    assert int(seg2['ISA'][13]) == int(ta2['reference'])


def test_partner_ids_without_idmode(botsenv):
    ta_info, seg = x12_envelope(frompartner='PLAINS', topartner='PLAINR')
    assert (seg['ISA'][6].strip(), seg['ISA'][8].strip(), seg['GS'][2], seg['GS'][3]) == ('PLAINS', 'PLAINR', 'PLAINS', 'PLAINR')
    assert ta_info['frompartner_outer'] == ta_info['frompartner_inner'] == 'PLAINS'


def test_idmode_isa_qualifier_gs(botsenv):
    ta_info, seg = x12_envelope(frompartner='ISAS|01|GSS', topartner='ISAR|14|GSR', messagetype='850004010IDM')
    assert (seg['ISA'][5], seg['ISA'][6].strip(), seg['ISA'][7], seg['ISA'][8].strip()) == ('01', 'ISAS', '14', 'ISAR')
    assert (seg['GS'][2], seg['GS'][3]) == ('GSS', 'GSR')
    assert ta_info['frompartner'] == 'ISAS|01|GSS', 'the partner id in the database is not changed'


def test_idmode_isa_qualifier(botsenv):
    _ta, seg = x12_envelope(frompartner='ISAS|01', topartner='ISAR|14', messagetype='850004010IDQ')
    assert (seg['ISA'][5], seg['ISA'][6].strip(), seg['ISA'][7], seg['ISA'][8].strip()) == ('01', 'ISAS', '14', 'ISAR')
    assert (seg['GS'][2], seg['GS'][3]) == ('ISAS', 'ISAR')


def test_idmode_partner_in_wrong_format(botsenv):
    from bots.exceptions import OutMessageError
    with pytest.raises(OutMessageError, match='ISA_qualifier_GS'):
        x12_envelope(frompartner='ONLYONE', topartner='ISAR|14|GSR', messagetype='850004010IDM')


# ---------------------------------------------------------------- counters

def counter(domain):
    from bots import botslib
    rows = list(botslib.query('SELECT nummer FROM uniek WHERE domein=%(domein)s', {'domein': domain}))
    return rows[0]['nummer'] if rows else None


def test_unique_continues_an_existing_counter(botsenv):
    from bots import botslib
    for _ in range(41):
        last = botslib.unique('utcounter_OLD')
    assert last == 41
    assert botslib.unique('utcounter_NEW_X', seedfrom='utcounter_OLD') == 42
    assert botslib.unique('utcounter_NEW_X', seedfrom='utcounter_OLD') == 43
    assert counter('utcounter_OLD') == 41, 'the counter that is continued is not changed'
    assert botslib.unique('utcounter_FRESH', seedfrom='utcounter_DOESNOTEXIST') == 1
    assert botslib.unique('utcounter_SAME', seedfrom='utcounter_SAME') == 1


def test_counter_per_partner_continues_the_bots3_counter(botsenv):
    """bots 3 with interchangecontrolperpartner: isacounter_<topartner>; now isacounter_<sender>_<receiver>"""
    from bots import botsglobal, botslib
    for _ in range(7):
        botslib.unique('isacounter_PPRECEIVER')
    botsglobal.ini.set('settings', 'interchangecontrolperpartner', 'True')
    try:
        ta1, _seg = x12_envelope(frompartner='PPSENDER', topartner='PPRECEIVER')
        ta2, _seg = x12_envelope(frompartner='PPSENDER', topartner='PPRECEIVER')
    finally:
        botsglobal.ini.set('settings', 'interchangecontrolperpartner', 'False')
    assert (ta1['reference'], ta2['reference']) == ('8', '9')
    assert counter('isacounter_PPSENDER_PPRECEIVER') == 9


# ---------------------------------------------------------------- merge

def test_merge_keeps_messages_with_different_envelope_data_apart(botsenv):
    from bots import botslib, envelope
    from bots.botsconfig import DONE, MERGED, OK, TRANSLATED
    start = max([row['idta'] for row in botslib.query('SELECT idta FROM ta')] or [0])
    content = [json.dumps({'envelope_content': [{}, {'GS02': gs02}, {}, {}]}) for gs02 in ('DIVISIONA', 'DIVISIONB')]
    sources = []
    for nr, rsrv5 in enumerate([content[0], content[1], content[0], content[1], content[0]]):
        ta = botslib.NewTransaction(
            status=TRANSLATED, statust=OK, idroute='utmerge', editype='x12', messagetype='850004010', envelope='x12',
            frompartner='MERGES', topartner='MERGER', testindicator='', charset='us-ascii', nrmessages=1, merge=True,
            filename=datafile(MESSAGE.replace('0001', '%04d' % (nr + 1))), rsrv3='', rsrv5=rsrv5)
        sources.append(ta.idta)
    # the same messages in another route are not touched
    other = botslib.NewTransaction(
        status=TRANSLATED, statust=OK, idroute='utother', editype='x12', messagetype='850004010', envelope='x12',
        frompartner='MERGES', topartner='MERGER', testindicator='', charset='us-ascii', nrmessages=1, merge=True,
        filename=datafile(), rsrv3='', rsrv5=content[0])

    envelope.mergemessages(TRANSLATED, MERGED, 'utmerge', rootidta=start)

    merged = list(botslib.query(
        'SELECT idta, filename, nrmessages, statust, errortext FROM ta WHERE idta>%(start)s AND status=%(status)s ORDER BY idta',
        {'start': start, 'status': MERGED}))
    assert [(row['statust'], row['nrmessages']) for row in merged] == [(OK, 3), (OK, 2)], [row['errortext'] for row in merged]
    for row, gs02, numbers in zip(merged, ('DIVISIONA', 'DIVISIONB'), (['0001', '0003', '0005'], ['0002', '0004'])):
        text = read(row['filename'])
        assert segments(text)['GS'][2] == gs02
        assert segments(text)['GE'][1] == str(len(numbers))
        assert [s.split('*')[2] for s in text.split('~') if s.strip().startswith('ST*')] == numbers
    children = dict((row['idta'], (row['child'], row['statust'])) for row in botslib.query(
        'SELECT idta, child, statust FROM ta WHERE idta>%(start)s AND status=%(status)s', {'start': start, 'status': TRANSLATED}))
    first, second = merged[0]['idta'], merged[1]['idta']
    assert [children[idta] for idta in sources] == [(first, DONE), (second, DONE), (first, DONE), (second, DONE), (first, DONE)]
    assert children[other.idta][1] == OK

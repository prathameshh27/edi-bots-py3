"""Behaviour carried over from the Bots 3.2.0 release and from a patched Bots 3 installation:
xml via editype 'mailbag', values in persist written by python 2, partner of a mail address via the CC field."""
import datetime
import decimal

import pytest

from helpers import parse, records, write_grammar

XML_GRAMMAR = '''
    from bots.botsconfig import *
    syntax = {}
    structure = [{ID: '%(root)s', MIN: 1, MAX: 1, LEVEL: [{ID: 'line', MIN: 0, MAX: 99}]}]
    recorddefs = {
        '%(root)s': [['BOTSID', 'M', 20, 'A'], ['nr', 'C', 35, 'AN'], ['kind', 'C', 35, 'AN']],
        'line': [['BOTSID', 'M', 20, 'A'], ['item', 'C', 35, 'AN']],
    }
'''
ORDER = '<?xml version="1.0"?><order><nr>1</nr><line><item>a</item></line><line><item>b</item></line></order>'
NOTE = '<note><nr>7</nr><kind>credit</kind></note>'


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    write_grammar('xml', 'ut_mb_order', XML_GRAMMAR % {'root': 'order'})
    write_grammar('xml', 'ut_mb_note', XML_GRAMMAR % {'root': 'note'})
    write_grammar('xml', 'ut_mb_other', XML_GRAMMAR % {'root': 'note'})
    write_grammar('xml', 'mailbag', '''
        mailbagsearch = [
            {'xpath': 'kind', 'content': 'debit', 'messagetype': 'ut_mb_other'},
            {'xpath': '.', 'tag': 'note', 'messagetype': 'ut_mb_note'},
            {'xpath': 'line', 'messagetype': 'ut_mb_order'},
        ]
        ''')


# ---------------------------------------------------------------- xml as 'mailbag'

@pytest.mark.parametrize('content, messagetype, first', [
    (ORDER, 'ut_mb_order', {'BOTSID': 'order', 'nr': '1'}),
    (NOTE, 'ut_mb_note', {'BOTSID': 'note', 'nr': '7', 'kind': 'credit'}),
    (NOTE.replace('credit', 'debit'), 'ut_mb_other', {'BOTSID': 'note', 'nr': '7', 'kind': 'debit'}),
])
def test_file_with_editype_mailbag_is_read_as_xml(botsenv, tmp_path, content, messagetype, first):
    """editype 'mailbag' at the parser: xml, messagetype found via grammars/xml/mailbag.py"""
    edi = parse(tmp_path, 'mailbag', 'mailbag', content)
    edi.checkforerrorlist()
    assert (edi.ta_info['editype'], edi.ta_info['messagetype']) == ('xml', messagetype)
    assert records(edi)[0] == first


def test_editype_mailbag_with_a_messagetype(botsenv, tmp_path):
    edi = parse(tmp_path, 'mailbag', 'ut_mb_order', ORDER)
    edi.checkforerrorlist()
    assert edi.ta_info['editype'] == 'xml'
    assert [record['BOTSID'] for record in records(edi)] == ['order', 'line', 'line']


def test_xml_mailbag_without_a_match_is_an_error(botsenv, tmp_path):
    from bots.exceptions import MessageError
    edi = parse(tmp_path, 'mailbag', 'mailbag', '<unknown><nr>1</nr></unknown>')
    with pytest.raises(MessageError, match='Could not find right xml messagetype'):
        edi.checkforerrorlist()


# ---------------------------------------------------------------- persist written by python 2

# pickle.dumps(value) of python 2.7 as it is in the column 'content'. Bots 3.2.0 stores it via latin-1;
# the release candidates of 3.2.0 store it as it is (the same text, as far as the pickle is ascii).
PYTHON2 = [
    ("S'abc'\np0\n.", 'abc'),
    ("Vcaf\xe9 \\u20ac\np0\n.", 'caf\xe9 \u20ac'),
    ("S'caf\\xc3\\xa9'\np0\n.", 'caf\xe9'),                    # str with utf-8 bytes
    ("S'caf\\xe9'\np0\n.", 'caf\xe9'),                          # str with latin-1 bytes
    ("(dp0\nS'a'\np1\n(lp2\nI1\naL2L\naF2.5\naNaI01\nasVk\xe9y\np3\n(S'x'\np4\nVy\np5\ntp6\ns.",
     {'a': [1, 2, 2.5, None, True], 'k\xe9y': ('x', 'y')}),
    ("cdatetime\ndatetime\np0\n(S'\\x07\\xe6\\x05\\x14\\r\\x0e\\x0f\\x00\\x00\\x00'\np1\ntp2\nRp3\n.",
     datetime.datetime(2022, 5, 20, 13, 14, 15)),
    ("cdecimal\nDecimal\np0\n(S'12.50'\np1\ntp2\nRp3\n.", decimal.Decimal('12.50')),
]


@pytest.mark.parametrize('number', range(len(PYTHON2)))
def test_persist_value_of_python2_is_read_and_can_be_updated(botsenv, number):
    from bots import botslib, transform
    content, value = PYTHON2[number]
    key = 'py2-%d' % number
    botslib.changeq('INSERT INTO persist (domein,botskey,content) VALUES (%(domein)s,%(botskey)s,%(content)s)',
                    {'domein': 'ut_carried', 'botskey': key, 'content': content})
    assert transform.persist_lookup('ut_carried', key) == value
    transform.persist_add_update('ut_carried', key, [value, 'new'])
    assert transform.persist_lookup('ut_carried', key) == [value, 'new']


def test_persist_keeps_non_ascii_text(botsenv):
    from bots import transform
    transform.persist_add('ut_carried', 'text', {'name': 'caf\xe9 \u20ac \u4e2d'})
    assert transform.persist_lookup('ut_carried', 'text') == {'name': 'caf\xe9 \u20ac \u4e2d'}
    assert transform.persist_lookup('ut_carried', 'not there') is None


# ---------------------------------------------------------------- partner of a mail address

@pytest.fixture(scope='module')
def mailchannel(botsenv):
    from bots import communication, models
    for idpartner, mail, cc, active in (
            ('UT_A', 'orders@a.example', 'boss@a.example, Admin@A.example', True),
            ('UT_B', 'first@b.example,second@b.example', '', True),
            ('UT_C', 'jorders@a.example', 'xboss@a.example', True),
            ('UT_OFF', 'off@d.example', 'cc@d.example', False)):
        models.partner(idpartner=idpartner, name=idpartner, active=active, mail=mail, cc=cc).save()
    channel = communication._comsession.__new__(communication._comsession)      # pylint: disable=protected-access
    channel.channeldict = {'idchannel': 'ut_not_there'}
    return channel


@pytest.mark.parametrize('address, idpartner', [
    ('orders@a.example', 'UT_A'),
    ('ORDERS@A.example', 'UT_A'),
    ('boss@a.example', 'UT_A'),                 # in the CC field, as bots 3.2.0
    ('admin@a.example', 'UT_A'),
    ('second@b.example', 'UT_B'),               # one of the addresses of a partner
    ('jorders@a.example', 'UT_C'),
    ('xboss@a.example', 'UT_C'),
    ('ss@a.example', None),                     # part of an address is not that address
    ('cc@d.example', None),                     # partner is not active
    ('nobody@a.example', None),
    ('%', None),
])
def test_partner_of_a_mail_address(mailchannel, address, idpartner):
    assert mailchannel.mailaddress2idpartner(address) == idpartner


# ---------------------------------------------------------------- xml attributes

@pytest.mark.parametrize('editype', ['xml', 'xmlnocheck'])
def test_xml_attributes_are_written_alphabetically_as_bots3_did(botsenv, editype):
    """whatever the order of the puts in the mapping (python 2 sorted them, python 3 does not by itself)"""
    from helpers import new_out, written
    write_grammar(editype, 'ut_attr', '''
        from bots.botsconfig import *
        syntax = {'indented': False}
        structure = [{ID: 'msg', MIN: 1, MAX: 1}]
        recorddefs = {'msg': [['BOTSID', 'M', 20, 'A'], ['msg__version', 'C', 9, 'AN'], ['msg__batch', 'C', 9, 'AN'],
                              ['contact', 'C', 35, 'AN'], ['contact__phone', 'C', 20, 'AN'],
                              ['contact__name', 'C', 20, 'AN'], ['contact__email', 'C', 40, 'AN']]}
        ''')
    out = new_out(editype, 'ut_attr')
    out.put({'BOTSID': 'msg', 'msg__version': '1.0', 'contact__phone': '1', 'contact': 'x', 'contact__name': 'n',
             'msg__batch': 'b', 'contact__email': 'e'})
    out.writeall()
    assert written(out).split(b'?>')[-1].strip() == \
        b'<msg batch="b" version="1.0"><contact email="e" name="n" phone="1">x</contact></msg>'


# ---------------------------------------------------------------- object of a database channel, written by python 2

# pickle.dumps(rows, protocol) of python 2.7 for rows as a MySQL DictCursor gives them (protocol 0 and 2)
DB_OBJECT_PYTHON2 = (
    '286c70300a286470310a53276e6f7465270a70320a4e7353276c696e655f6964270a70330a56310a70340a73532773686970706564270a'
    '70350a4c334c0a7353276e616d65270a70360a56636166e90a70370a735327706f5f64617465270a70380a636461746574696d650a6461'
    '74650a70390a2853275c7830375c7865365c7830355c783134270a7031300a747031310a527031320a735327706f5f6e756d626572270a'
    '7031330a56504f310a7031340a735327726177270a7031350a53276361665c7863335c786139270a7031360a7353276372656174656427'
    '0a7031370a636461746574696d650a6461746574696d650a7031380a2853275c7830375c7865365c7830355c7831345c725c7830655c78'
    '30665c7830305c7830305c783030270a7031390a747032300a527032310a7353277175616e74697479270a7032320a63646563696d616c'
    '0a446563696d616c0a7032330a28532731322e3530270a7032340a747032350a527032360a73612e',
    '80025d71007d71012855046e6f746571024e55076c696e655f69647103580100000031710455077368697070656471058a010355046e61'
    '6d6571065805000000636166c3a971075507706f5f646174657108636461746574696d650a646174650a7109550407e60514710a85710b'
    '52710c5509706f5f6e756d626572710d5803000000504f31710e5503726177710f5505636166c3a97110550763726561746564711163'
    '6461746574696d650a6461746574696d650a7112550a07e605140d0e0f000000711385711452711555087175616e746974797116636465'
    '63696d616c0a446563696d616c0a7117550531322e3530711885711952711a75612e')


@pytest.mark.parametrize('number', [0, 1])
def test_database_object_received_by_bots3_is_read(botsenv, tmp_path, number):
    """a file of a database channel that bots 3 received and did not translate yet (or that is re-received)"""
    import binascii
    edi = parse(tmp_path, 'db', 'ut_any', binascii.unhexlify(DB_OBJECT_PYTHON2[number]))
    assert edi.root == [{
        'po_number': 'PO1', 'line_id': '1', 'po_date': datetime.date(2022, 5, 20),
        'created': datetime.datetime(2022, 5, 20, 13, 14, 15), 'quantity': decimal.Decimal('12.50'), 'shipped': 3,
        'name': 'caf\xe9', 'note': None, 'raw': 'caf\xe9'}]

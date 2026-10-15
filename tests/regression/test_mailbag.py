"""A route with editype 'mailbag' receives xml files of several kinds (and edifact) in one channel."""
import os
import textwrap

GRAMMAR = '''
    from bots.botsconfig import *
    syntax = {'indented': False}
    structure = [{ID: '%(root)s', MIN: 1, MAX: 1, LEVEL: [{ID: 'line', MIN: 0, MAX: 99}]}]
    recorddefs = {
        '%(root)s': [['BOTSID', 'M', 20, 'A'], ['nr', 'C', 35, 'AN'], ['via', 'C', 35, 'AN']],
        'line': [['BOTSID', 'M', 20, 'A'], ['item', 'C', 35, 'AN']],
    }
'''
MAPPING = '''
    def main(inn, out):
        out.ta_info['botskey'] = inn.get({'BOTSID': '%(root)s', 'nr': None})
        out.put({'BOTSID': '%(root)s', 'nr': inn.get({'BOTSID': '%(root)s', 'nr': None}), 'via': '%(root)s'})
        for line in inn.getloop({'BOTSID': '%(root)s'}, {'BOTSID': 'line'}):
            lou = out.putloop({'BOTSID': '%(root)s'}, {'BOTSID': 'line'})
            lou.put({'BOTSID': 'line', 'item': line.get({'BOTSID': 'line', 'item': None})})
'''
FILES = {
    'order.xml': b'<?xml version="1.0" encoding="utf-8"?>\n<order><nr>11</nr><line><item>a</item></line></order>',
    'bom.xml': b'\xef\xbb\xbf<order><nr>12</nr><line><item>b</item></line><line><item>c</item></line></order>',
    'note.xml': b'  \r\n<note><nr>21</nr></note>',
}


def usersys(botsrun, kind, name, text):
    directory = os.path.join(botsrun.envdir, 'usersys', *kind.split('/'))
    os.makedirs(directory, exist_ok=True)
    init = os.path.join(directory, '__init__.py')
    if not os.path.exists(init):
        open(init, 'w', encoding='utf8').close()
    with open(os.path.join(directory, name + '.py'), 'w', encoding='utf8') as f:
        f.write(textwrap.dedent(text))


def prepare(botsrun, files, routes):
    src, out = botsrun.path('src'), botsrun.path('out')
    for name, content in files.items():
        with open(os.path.join(src, name), 'wb') as f:
            f.write(content)
    for root in ('order', 'note'):
        usersys(botsrun, 'grammars/xml', 'mb_' + root, GRAMMAR % {'root': root})
        usersys(botsrun, 'mappings/xml', 'mb_' + root, MAPPING % {'root': root})
    usersys(botsrun, 'grammars/xml', 'mailbag', '''
        mailbagsearch = [
            {'xpath': '.', 'tag': 'note', 'messagetype': 'mb_note'},
            {'xpath': 'line', 'messagetype': 'mb_order'},
        ]
        ''')
    botsrun.configure(
        channels=[dict(idchannel='mb_in', inorout='in', type='file', path=src, filename='*'),
                  dict(idchannel='mb_out', inorout='out', type='file', path=out, filename='{botskey}.xml')],
        routes=routes,
        translate=[dict(active=True, fromeditype='xml', frommessagetype='mb_' + root, tscript='mb_' + root,
                        toeditype='xml', tomessagetype='mb_' + root) for root in ('order', 'note')])
    return out


def outfiles(out):
    found = {}
    for name in os.listdir(out):
        with open(os.path.join(out, name), 'rb') as f:
            found[name] = f.read().split(b'?>')[-1].strip()
    return found


EXPECTED = {
    '11.xml': b'<order><nr>11</nr><via>order</via><line><item>a</item></line></order>',
    '12.xml': b'<order><nr>12</nr><via>order</via><line><item>b</item></line><line><item>c</item></line></order>',
    '21.xml': b'<note><nr>21</nr><via>note</via></note>',
}


def test_xml_files_in_a_mailbag_route(botsrun):
    out = prepare(botsrun, FILES, [
        dict(idroute='mb', seq=1, active=True, fromchannel='mb_in', fromeditype='mailbag', frommessagetype='mailbag',
             translateind=1, tochannel='mb_out', toeditype='xml')])
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    assert outfiles(out) == EXPECTED


def test_mailbag_route_in_parts_and_a_file_that_is_no_edi(botsrun):
    """As in a bots 3 installation: one route part receives ('mailbag', no translation), the next translates, the
    last sends. A file that is not xml, edifact, x12 or tradacoms is an error; the other files are processed."""
    files = dict(FILES, **{'text.txt': b'this is not an edi file'})
    out = prepare(botsrun, files, [
        dict(idroute='mb', seq=100, active=True, fromchannel='mb_in', fromeditype='mailbag',
             frommessagetype='mailbag', translateind=0),
        dict(idroute='mb', seq=200, active=True, translateind=1),
        dict(idroute='mb', seq=300, active=True, translateind=0, tochannel='mb_out', toeditype='xml')])
    botsrun.engine()
    result = botsrun.result()
    assert result['files'] == [['bom.xml', 3], ['note.xml', 3], ['order.xml', 3], ['text.txt', 1]], botsrun.root
    assert len(result['errors']) == 1 and '[M51]' in result['errors'][0], result['errors']
    assert outfiles(out) == EXPECTED

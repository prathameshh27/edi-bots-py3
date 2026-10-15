"""Json without the name of the root for a whole installation: syntax 'named_root_object' in the envelope grammar
(usersys/grammars/json/json.py, usersys/grammars/jsonnocheck/json.py) is the default of all grammars of that
editype."""
import json
import os
import textwrap

GRAMMAR = '''
    from bots.botsconfig import *
    syntax = {%s}
    structure = [{ID: 'order', MIN: 1, MAX: 1, LEVEL: [{ID: 'line', MIN: 0, MAX: 99}]}]
    recorddefs = {
        'order': [['BOTSID', 'M', 20, 'A'], ['nr', 'C', 35, 'AN']],
        'line': [['BOTSID', 'M', 20, 'A'], ['item', 'C', 35, 'AN']],
    }
'''
MAPPING = '''
    def main(inn, out):
        out.put({'BOTSID': 'order', 'nr': inn.get({'BOTSID': 'order', 'nr': None})})
        for line in inn.getloop({'BOTSID': 'order'}, {'BOTSID': 'line'}):
            lou = out.putloop({'BOTSID': 'order'}, {'BOTSID': 'line'})
            lou.put({'BOTSID': 'line', 'item': line.get({'BOTSID': 'line', 'item': None})})
'''
NO_ROOT_NAME = "syntax = {'named_root_object': False}\n"
CONTENT = {'nr': '5', 'line': [{'item': 'a'}, {'item': 'b'}]}
TARGETS = {'jr_default': 'json', 'jr_named': 'json', 'jr_free': 'jsonnocheck'}        # messagetype: editype


def usersys(botsrun, kind, name, text):
    directory = os.path.join(botsrun.envdir, 'usersys', *kind.split('/'))
    os.makedirs(directory, exist_ok=True)
    init = os.path.join(directory, '__init__.py')
    if not os.path.exists(init):
        open(init, 'w', encoding='utf8').close()
    with open(os.path.join(directory, name + '.py'), 'w', encoding='utf8') as f:
        f.write(textwrap.dedent(text))


def run(botsrun):
    src = botsrun.path('src')
    with open(os.path.join(src, 'order.json'), 'w', encoding='utf8') as f:
        json.dump({'order': CONTENT}, f)
    usersys(botsrun, 'grammars/json', 'jr_default', GRAMMAR % '')
    usersys(botsrun, 'grammars/json', 'jr_named', GRAMMAR % "'named_root_object': True")
    usersys(botsrun, 'grammars/jsonnocheck', 'jr_free', 'syntax = {}\n')
    usersys(botsrun, 'mappings/json', 'jr_copy', MAPPING)
    channels = [dict(idchannel='jr_in', inorout='in', type='file', path=src, filename='*.json')]
    routes, translate = [], []
    for target, editype in TARGETS.items():
        channels.append(dict(idchannel='out_' + target, inorout='out', type='file', path=botsrun.path('out', target),
                             filename='order.json'))
        routes.append(dict(idroute=target, seq=1, active=True, fromchannel='jr_in', fromeditype='json',
                           frommessagetype='jr_default', translateind=1, alt=target, tochannel='out_' + target,
                           toeditype=editype))
        translate.append(dict(active=True, fromeditype='json', frommessagetype='jr_default', alt=target,
                              tscript='jr_copy', toeditype=editype, tomessagetype=target))
    botsrun.configure(channels=channels, routes=routes, translate=translate)
    code = botsrun.engine()
    result = botsrun.result()
    assert code == 0 and result['report']['lasterror'] == 0, (botsrun.root, result['errors'])
    written = {}
    for target in TARGETS:
        with open(os.path.join(botsrun.path('out', target), 'order.json'), encoding='utf8') as f:
            written[target] = json.load(f)
    return written


def test_root_is_named_by_default(botsrun):
    assert run(botsrun) == {'jr_default': {'order': CONTENT}, 'jr_named': {'order': CONTENT},
                            'jr_free': {'order': CONTENT}}


def test_root_without_name_for_all_grammars_of_an_installation(botsrun):
    usersys(botsrun, 'grammars/json', 'json', NO_ROOT_NAME)
    usersys(botsrun, 'grammars/jsonnocheck', 'json', NO_ROOT_NAME)
    # a grammar that says otherwise keeps the name
    assert run(botsrun) == {'jr_default': CONTENT, 'jr_named': {'order': CONTENT}, 'jr_free': CONTENT}

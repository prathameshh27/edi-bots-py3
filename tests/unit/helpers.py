"""Helpers for unit tests: write a grammar into the test environment, parse a file, write a message."""
import itertools
import json
import os
import textwrap

_counter = itertools.count(1000)


def write_grammar(editype, name, text, kind='grammars'):
    """Write usersys/<kind>/<editype>/<name>.py in the environment of the test session."""
    from bots import botsglobal
    directory = os.path.join(botsglobal.ini.get('directories', 'usersysabs'), kind, editype)
    os.makedirs(directory, exist_ok=True)
    init = os.path.join(directory, '__init__.py')
    if not os.path.exists(init):
        open(init, 'w', encoding='utf8').close()
    with open(os.path.join(directory, name + '.py'), 'w', encoding='utf8') as f:
        f.write(textwrap.dedent(text).lstrip('\n'))
    botsglobal.not_import.discard('.'.join((botsglobal.usersysimportpath, kind, editype, name)))


def parse(tmp_path, editype, messagetype, content, **ta_info):
    """Parse content (str or bytes) with a grammar; returns the inmessage object (errors not raised)."""
    from bots import inmessage
    path = str(tmp_path / ('in%d.edi' % next(_counter))).replace('\\', '/')
    with open(path, 'wb') as f:
        f.write(content if isinstance(content, bytes) else content.encode('utf-8'))
    return inmessage.parse_edi_file(editype=editype, messagetype=messagetype, filename=path, **ta_info)


def records(edi):
    """All records of a parsed file as a flat list of dicts (without the bots-internal BOTSIDnr)."""
    found = []

    def walk(node):
        if node.record:
            found.append(dict((k, v) for k, v in node.record.items() if k != 'BOTSIDnr'))
        for child in node.children:
            walk(child)
    walk(edi.root)
    return found


def new_out(editype, messagetype, **ta_info):
    """An outmessage object writing to a file in the data directory of the test environment."""
    from bots import outmessage
    return outmessage.outmessage_init(
        editype=editype, messagetype=messagetype, filename=str(next(_counter)),
        reference='1', statust=3, divtext='', **ta_info)


def written(out):
    """Content of the file an outmessage object wrote, as bytes."""
    from bots import botslib
    with open(botslib.abspathdata(out.ta_info['filename']), 'rb') as f:
        return f.read()


def written_json(out):
    return json.loads(written(out).decode('utf-8'))

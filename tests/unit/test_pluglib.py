"""pluglib: reading plugin indexes written by bots 2/3, and guarding what a plugin may write."""
import datetime
import io
import os
import zipfile

import pytest

INDEX_PY2 = '''# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
version = u'3.2.0'
plugins = [
{u'plugintype': u'channel', u'idchannel': u'ut_in', u'inorout': u'in', u'type': u'file', u'path': u'botssys/infile/ut',
 u'filename': u'*.edi', u'port': 0L, u'remove': False, u'rsrv2': None, u'desc': u'M\\xfcller 10L'},
{u'plugintype': u'partner', u'idpartner': u'UT_PARTNER', u'active': True, u'isgroup': False, u'name': u'x',
 u'startdate': datetime.date(2014, 1, 31), u'attr5': u'', u'group': []},
]
'''


def test_parse_python_index_with_py2_literals(botsenv):
    from bots import pluglib
    index = pluglib.parse_python_botsindex(INDEX_PY2)
    assert index['version'] == '3.2.0'
    channel, partner = index['plugins']
    assert channel['port'] == 0 and channel['remove'] is False and channel['rsrv2'] is None
    assert channel['desc'] == 'M\xfcller 10L'           # 'L' inside a string is left alone
    assert partner['startdate'] == datetime.date(2014, 1, 31)


@pytest.mark.parametrize('source', [
    "import os\nplugins = [os.getcwd()]",                    # call of something else than datetime
    "plugins = [__import__('os').system('echo x')]",
    "plugins = []\nopen('x', 'w')",                          # statement that is not an assignment
    "plugins = [x for x in range(3)]",
    "version = '3'",                                         # no plugins
    "plugins = [{'a': 1}",                                   # not valid python
])
def test_python_index_is_parsed_not_executed(botsenv, source):
    from bots import pluglib
    from bots.exceptions import PluginError
    with pytest.raises(PluginError):
        pluglib.parse_python_botsindex(source)


def test_version_tuple(botsenv):
    from bots.pluglib import version_tuple
    assert version_tuple('3.10') > version_tuple('3.4')
    assert version_tuple('3.2.0rc2') == (3, 2, 0)
    assert version_tuple('4.0.0rc4+source') == (4, 0, 0)
    assert version_tuple(2) == (2,) and version_tuple('unknown') == ()
    assert version_tuple('unknown') < (3, 4)


def make_plugin(path, index, files):
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('botsindex.py', index)
        for name, content in files.items():
            z.writestr(name, content)


def test_read_plugin_with_long_literals_and_data_files(botsenv, tmp_path):
    from bots import models, pluglib
    plugin = str(tmp_path / 'p.zip')
    make_plugin(plugin, INDEX_PY2, {
        'usersys/mappings/xml/ut_map.py': 'def main(inn, out):\n    pass\n',
        'usersys/mappings/xml/ut_schema.xsd': '<schema/>',
        'botssys/infile/ut/in.edi': 'x',
    })
    report = pluglib.read_plugin(plugin)
    assert models.channel.objects.filter(idchannel='ut_in').exists()
    assert models.partner.objects.get(idpartner='UT_PARTNER').startdate == datetime.date(2014, 1, 31)
    usersys = os.path.join(botsenv, 'usersys')
    assert os.path.isfile(os.path.join(usersys, 'mappings', 'xml', 'ut_map.py'))
    assert os.path.isfile(os.path.join(usersys, 'mappings', 'xml', 'ut_schema.xsd')), 'data file next to a mapping is installed'
    assert os.path.isfile(os.path.join(botsenv, 'botssys', 'infile', 'ut', 'in.edi'))
    assert not report['skipped']


def test_plugin_cannot_write_outside_environment(botsenv, tmp_path):
    from bots import pluglib
    plugin = str(tmp_path / 'slip.zip')
    index = "version = '3.2.0'\nplugins = [{'plugintype': 'channel', 'idchannel': 'ut_slip', 'inorout': 'in', 'type': 'file'}]\n"
    make_plugin(plugin, index, {
        'usersys/../../ut_escaped.py': 'x = 1\n',
        'usersys/grammars/../../config/ut_planted.py': 'x = 1\n',
        'botssys/../../ut_escaped.txt': 'x',
        'usersys/mappings/xml/ut_ok.py': 'x = 1\n',
    })
    report = pluglib.read_plugin(plugin)
    assert len(report['skipped']) == 3
    assert not os.path.exists(os.path.join(os.path.dirname(botsenv), 'ut_escaped.py'))
    assert not os.path.exists(os.path.join(os.path.dirname(botsenv), 'ut_escaped.txt'))
    assert not os.path.exists(os.path.join(botsenv, 'config', 'ut_planted.py'))
    assert os.path.isfile(os.path.join(botsenv, 'usersys', 'mappings', 'xml', 'ut_ok.py'))


def test_failed_plugin_leaves_nothing_in_database(botsenv, tmp_path):
    from bots import models, pluglib
    from bots.exceptions import PluginError
    plugin = str(tmp_path / 'partial.zip')
    index = ("version = '3.2.0'\nplugins = [\n"
             "{'plugintype': 'channel', 'idchannel': 'ut_partial', 'inorout': 'in', 'type': 'file'},\n"
             "{'plugintype': 'chanpar', 'idpartner': 'UT_DOES_NOT_EXIST', 'mail': 'x@example.com'},\n]\n")   # no idchannel
    make_plugin(plugin, index, {})
    with pytest.raises(PluginError):
        pluglib.read_plugin(plugin)
    assert not models.channel.objects.filter(idchannel='ut_partial').exists()

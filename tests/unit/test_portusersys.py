"""bots-portusersys: user scripts of bots 3 (python 2) to python 3; bots-checkusersys."""
import os
import subprocess
import sys
import textwrap
import zipfile

import pytest

from bots import portusersys

MAPPING_PY2 = textwrap.dedent('''\
    #mapping script of bots 3
    import bots.transform as transform
    from recordsD96AUN import recorddefs
    import helper

    def main(inn,out):
        lines = {}
        for lin in inn.getloop({'BOTSID':'UNH'},{'BOTSID':'LIN'}):
            nr = unicode(lin.get({'BOTSID':'LIN','1082':None}))
            if lines.has_key(nr):
                print 'double line', nr
            lines[nr] = long(1)
        for key, value in lines.iteritems():
            try:
                out.put({'BOTSID':'HEA','NR':key})
            except Exception, msg:
                raise transform.botslib.BotsError(u'error %s' % msg)
        names = lines.keys()
        names.sort()
        return sorted(set(names))
    ''')


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(content if isinstance(content, bytes) else content.encode('utf-8'))


@pytest.fixture
def usersys(tmp_path):
    source = str(tmp_path / 'old')
    write(os.path.join(source, 'mappings', 'edifact', 'orders2fixed.py'), MAPPING_PY2)
    write(os.path.join(source, 'mappings', 'edifact', 'recordsD96AUN.py'), 'recorddefs = {}\n')
    write(os.path.join(source, 'mappings', 'edifact', 'helper.py'), 'def help():\n    return 1\n')
    write(os.path.join(source, 'mappings', 'edifact', '__init__.py'), '')
    write(os.path.join(source, 'mappings', 'edifact', 'modern.py'), 'import os\nVALUE = {"a": 1}\n')
    # latin-1, no coding line: python 2 accepts it, python 3 does not
    write(os.path.join(source, 'mappings', 'edifact', 'latin.py'), b"NAME = 'caf\xe9'  # caf\xe9\n")
    write(os.path.join(source, 'mappings', 'edifact', 'broken.py'), 'def main(inn, out):\n    return (((\n')
    write(os.path.join(source, 'mappings', 'edifact', 'old.pyc'), b'\x00\x01')
    write(os.path.join(source, 'grammars', 'templatehtml', 'templates', 'page.html'), '<html>caf\xe9</html>')
    return source


def test_port_of_a_directory(usersys, tmp_path):
    pytest.importorskip('fissix')
    destination = str(tmp_path / 'new')
    report = portusersys.port_tree(usersys, destination)

    with open(os.path.join(destination, 'mappings', 'edifact', 'orders2fixed.py'), encoding='utf8') as f:
        ported = f.read()
    compile(ported, 'orders2fixed.py', 'exec')
    assert 'from .recordsD96AUN import recorddefs' in ported and 'from . import helper' in ported
    assert 'import bots.transform as transform' in ported, 'imports of other modules are not changed'
    for python2 in ('unicode(', 'has_key', 'iteritems', 'long(', 'print \'', 'Exception, msg'):
        assert python2 not in ported, python2
    assert report.changed['mappings/edifact/orders2fixed.py'] == [
        '2 import(s) of a file next to it made explicit', 'python 2 -> python 3']

    # a file that is python 3 is copied as it is
    with open(os.path.join(destination, 'mappings', 'edifact', 'modern.py'), 'rb') as f:
        assert f.read() == b'import os\nVALUE = {"a": 1}\n'
    assert 'mappings/edifact/modern.py' not in report.changed
    # latin-1 without coding line: now utf-8
    with open(os.path.join(destination, 'mappings', 'edifact', 'latin.py'), 'rb') as f:
        assert f.read() == "NAME = 'caf\xe9'  # caf\xe9\n".encode('utf-8')
    # other files are copied, compiled files are not
    assert os.path.isfile(os.path.join(destination, 'grammars', 'templatehtml', 'templates', 'page.html'))
    assert not os.path.exists(os.path.join(destination, 'mappings', 'edifact', 'old.pyc'))
    assert report.skipped == ['mappings/edifact/old.pyc']
    # what can not be made python 3 is reported, and copied as it is
    assert list(report.errors) == ['mappings/edifact/broken.py']
    # lines to look at: .sort() on keys is converted by 2to3; the loop over a set is not
    reasons = ' '.join(why for _nr, _line, why in report.review['mappings/edifact/orders2fixed.py'])
    assert 'set' in reasons
    # the source is not changed
    with open(os.path.join(usersys, 'mappings', 'edifact', 'orders2fixed.py'), encoding='utf8') as f:
        assert f.read() == MAPPING_PY2
    assert report.python == 7 and report.files == 8


def test_port_of_a_plugin(usersys, tmp_path):
    pytest.importorskip('fissix')
    plugin = str(tmp_path / 'plugin.zip')
    index = "# -*- coding: utf-8 -*-\nversion = u'3.2.0'\nplugins = [{u'plugintype': u'routes', u'idroute': u'x', u'seq': 1L}]\n"
    with zipfile.ZipFile(plugin, 'w') as archive:
        archive.writestr('botsindex.py', index)
        for dirpath, _dirs, filenames in os.walk(usersys):
            for filename in filenames:
                full = os.path.join(dirpath, filename)
                archive.write(full, 'usersys/' + os.path.relpath(full, usersys).replace(os.sep, '/'))
    ported = str(tmp_path / 'plugin_py3.zip')
    report = portusersys.port_zip(plugin, ported)
    with zipfile.ZipFile(ported) as archive:
        names = archive.namelist()
        assert archive.read('botsindex.py').decode() == index, 'the index is data for bots: not changed'
        assert 'from .recordsD96AUN import' in archive.read('usersys/mappings/edifact/orders2fixed.py').decode()
    assert 'usersys/mappings/edifact/old.pyc' not in names and 'usersys/mappings/edifact/helper.py' in names
    assert 'usersys/mappings/edifact/orders2fixed.py' in report.changed
    assert not os.path.exists(ported + '.unzipped')


def test_port_of_grammars_that_go_into_a_usersys(tmp_path):
    """a library of grammars imports a file that is not in the library but in the usersys it is for"""
    library = str(tmp_path / 'library.zip')
    with zipfile.ZipFile(library, 'w') as archive:
        archive.writestr('edifact_D96A/ORDERSD96AUN.py',
                         'from bots.botsconfig import *\nfrom edifact import syntax\nfrom recordsD96AUN import recorddefs\n')
        archive.writestr('edifact_D96A/recordsD96AUN.py', 'recorddefs = {}\n')
    target = tmp_path / 'usersys' / 'grammars' / 'edifact'
    target.mkdir(parents=True)
    (target / 'edifact.py').write_text('syntax = {}\n')

    without = str(tmp_path / 'without')
    portusersys.port_zip(library, without)
    with open(os.path.join(without, 'edifact_D96A', 'ORDERSD96AUN.py'), encoding='utf8') as f:
        assert 'from edifact import syntax' in f.read(), 'edifact.py is not known: not changed'

    ported = str(tmp_path / 'ported')
    report = portusersys.port_zip(library, ported, target=str(target))
    with open(os.path.join(ported, 'edifact_D96A', 'ORDERSD96AUN.py'), encoding='utf8') as f:
        text = f.read()
    assert 'from .edifact import syntax' in text and 'from .recordsD96AUN import recorddefs' in text
    assert 'from bots.botsconfig import *' in text
    assert list(report.changed) == ['edifact_D96A/ORDERSD96AUN.py']


def test_command_line(usersys, tmp_path):
    pytest.importorskip('fissix')
    script = "import sys; sys.argv[0] = 'bots-portusersys'; from bots.portusersys import start; start()"
    destination = str(tmp_path / 'cli')
    done = subprocess.run([sys.executable, '-c', script, usersys, destination], capture_output=True, text=True)
    assert done.returncode == 1, done.stdout + done.stderr           # broken.py is not valid python
    assert '1 python files with an error' in done.stdout and 'mappings/edifact/broken.py' in done.stdout
    assert os.path.isfile(destination + '.review.txt')
    os.remove(os.path.join(usersys, 'mappings', 'edifact', 'broken.py'))
    done = subprocess.run([sys.executable, '-c', script, usersys, str(tmp_path / 'cli2')], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    # an existing destination is not overwritten
    done = subprocess.run([sys.executable, '-c', script, usersys, destination], capture_output=True, text=True)
    assert done.returncode == 2 and 'exists' in done.stdout


def test_check_usersys(botsenv):
    """the usersys of the test environment, with one grammar and one script that are wrong"""
    from helpers import write_grammar
    write_grammar('fixed', 'ut_check_ok', '''
        from bots.botsconfig import *
        structure = [{ID: 'HEA', MIN: 1, MAX: 1}]
        recorddefs = {'HEA': [['BOTSID', 'M', 3, 'A'], ['NR', 'C', 5, 'AN']]}
    ''')
    write_grammar('fixed', 'ut_check_wrong', '''
        from bots.botsconfig import *
        structure = [{ID: 'HEA', MIN: 1, MAX: 1}]
        recorddefs = {'XXX': [['BOTSID', 'M', 3, 'A'], ['NR', 'C', 5, 'AN']]}
    ''')
    write_grammar('fixed', 'ut_check_script', 'import module_that_is_not_there\n', kind='mappings')
    write_grammar('fixed', 'ut_check_python2', 'print "python 2"\n', kind='mappings')
    try:
        result = portusersys.check_usersys()
    finally:
        for kind, name in (('grammars', 'ut_check_wrong'), ('mappings', 'ut_check_script'),
                           ('mappings', 'ut_check_python2')):
            os.remove(os.path.join(botsenv, 'usersys', kind, 'fixed', name + '.py'))
    failed = dict((name, error) for _kind, name, error in result['failed'])
    assert 'grammars/fixed/ut_check_wrong.py' in failed and 'grammars/fixed/ut_check_ok.py' not in failed
    assert 'module_that_is_not_there' in failed['mappings/fixed/ut_check_script.py']
    assert [name for name, _error in result['notcompiled']] == ['mappings/fixed/ut_check_python2.py']
    assert result['grammars'] >= 2 and result['python'] >= 4


def test_division_of_whole_numbers_is_a_line_to_review():
    """7/2 is 3 in python 2 and 3.5 in python 3: a slice or range with it fails (2to3 does not change it)"""
    from bots import portusersys
    source = '\n'.join([
        'half = len(addresses)/2',              # 1: yes
        'first = addresses[:half]',
        'price = float(amount) / 100',          # 3: no
        'ratio = total / 2.0',                  # 4: no
        'count /= size',                        # 5: yes
        'pages = lines // 60',                  # 6: no
        "path = 'a/b'  # 1/2",                  # 7: no
        'amount = Decimal(text) / qty',         # 8: no
    ]) + '\n'
    assert portusersys.division_lines(source) == {1, 5}
    _data, _done, error, review = portusersys.port_source(source.encode('utf-8'), set(), 'mapping.py')
    assert not error
    assert [(number, why) for number, _line, why in review] == [(1, portusersys.DIVISION), (5, portusersys.DIVISION)]


def test_loop_over_a_dict_is_a_line_to_review():
    """the order of the keys differs between python 2 and 3: records written in the loop come in another order"""
    from bots import portusersys
    source = '\n'.join([
        "for qualifier, party in {'ST': 'ShipTo', 'BT': 'BillTo'}.items():",        # 1: yes
        '    pass',
        'for key in sorted(lookup):',                                                # 3: no
        '    pass',
        'for key in lookup.keys():',                                                 # 5: yes
        '    pass',
        "for line in inn.getloop({'BOTSID': 'order'}, {'BOTSID': 'line'}):",         # 7: no (bots loop)
        '    pass',
    ]) + '\n'
    review = portusersys.port_source(source.encode('utf-8'), set(), 'mapping.py')[3]
    assert [number for number, _line, why in review if why.startswith('loop over a dict')] == [1, 5]

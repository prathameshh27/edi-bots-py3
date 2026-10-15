"""
Port user scripts of bots 3 (python 2) to this version of bots (python 3), and check a usersys.

bots-portusersys: converts a usersys directory, a plugin (zip) or a directory/zip with grammars:
    - imports of a file next to it:  'from recordsD96AUN import recorddefs' -> 'from .recordsD96AUN import ...'
    - python 2 syntax and names (print, except X, e, unicode, has_key, iteritems, ...): needs python
      library 'fissix' (pip install bots-ediint[port]); files that are python 3 already are not touched;
    - a file that is not utf-8 and has no coding line is written as utf-8;
    - every file is compiled with this python;
    - lines that are valid python 3 but can work differently are listed for review.
  The source is never changed.

bots-checkusersys: checks the usersys of an environment as bots-engine uses it: every python file is
  compiled, every grammar is read (same checks as in a translation), every script is imported.
"""
# pylint: disable=missing-function-docstring
import ast
import concurrent.futures
import io
import json
import os
import re
import shutil
import sys
import tokenize
import zipfile

# python 2 only: reason to run the 2to3-conversion on a file
PY2_HINTS = re.compile(
    r'''\bunicode\s*\(|\bbasestring\b|\bxrange\s*\(|\blong\s*\(|\bunichr\s*\(|\braw_input\s*\(|\.has_key\s*\('''
    r'''|\.iter(items|keys|values)\s*\(|\.view(items|keys|values)\s*\(|^\s*print\s+[^(=\s]|^\s*print\s*$'''
    r'''|^\s*print\s*>>|\bexcept\s+[\w.]+\s*,\s*\w+\s*:|\braise\s+[\w.]+\s*,'''
    r'''|\bimport\s+(cPickle|cStringIO|StringIO|urllib2|urlparse|ConfigParser|Queue|httplib|xmlrpclib|commands)\b'''
    r'''|\bfrom\s+(cPickle|cStringIO|StringIO|urllib2|urlparse|ConfigParser|Queue|httplib|xmlrpclib)\s+import\b'''
    r'''|\bexecfile\s*\(|\breduce\s*\(|\bstring\.(letters|maketrans|uppercase|lowercase|join|split|replace|strip)\b'''
    r'''|\bos\.getcwdu\b|\.next\s*\(\s*\)|\bfile\s*\(|\bapply\s*\(|\bdict\.has_key''',
    re.MULTILINE)

# valid python 3, but the result can be another than in python 2: (pattern, what to check)
REVIEW = [
    (re.compile(r'\.sort\s*\(\s*(cmp\s*=|[A-Za-z_]\w*\s*\))|\bsorted\s*\([^)]*\bcmp\s*=|(?<![\w.])cmp\s*\('),
     'cmp is not in python 3: use key=...'),
    (re.compile(r'\.(encode|decode)\s*\('),
     'encode/decode: in python 3 text is str and data is bytes; in bots 4 values in a mapping are str'),
    (re.compile(r'''\bopen\s*\([^)]*['"][rwa]b\+?['"]'''),
     'file opened as binary: reading gives bytes, not str'),
    (re.compile(r'(?<![\w.])set\s*\(|\bfrozenset\s*\('),
     'set: the order of looping over a set is not the order of python 2 and can change per run; use sorted()'),
    (re.compile(r'\.(keys|values|items)\s*\(\s*\)\s*(\[|\.sort\b)'),
     'keys()/values()/items() is not a list in python 3'),
    (re.compile(r'\bfor\b[^:#]*\bin\b([^#]*\.(items|keys|values)\s*\(\s*\)|\s*(list\s*\(\s*)?\{[^}]*:)'),
     'loop over a dict: python 2 gave the keys in an arbitrary (but fixed) order, python 3 in the order they '
     'were added; what the loop writes can come in another order'),
    (re.compile(r'''['"]noBOTSID['"]\s*:\s*[1-9]'''),
     "'noBOTSID': 1 in bots 4 is: field 1 has the record ID; use True for 'records have no record ID'"),
    (re.compile(r'\b(map|filter|zip)\s*\([^)]*\)\s*(\[|\.)'),
     'map/filter/zip do not give a list in python 3'),
    (re.compile(r'(?<![\w.])pickle\.|\bpersist_lookup\b'),
     'pickle/persist: values stored by python 2 may not be readable'),
    (re.compile(r'\boutmessage\.var\b|\bmessagegrammarread\b'),
     'changed in bots 4'),
    (re.compile(r'\bbotslib\.(runexternprogram|unicode|readdata|opendata)\b|\breaddata\s*\('),
     'check: botslib.readdata/opendata give str, readdata_bin/opendata_bin give bytes'),
]
SKIP_DIRS = ('__pycache__', '.git', '.svn', '.hg')


def refactoringtool():
    """the 2to3 converter, or None if not installed."""
    for package in ('fissix', 'lib2to3'):
        try:
            refactor = __import__(package + '.refactor', fromlist=['refactor'])
        except ImportError:
            continue
        fixers = [fixer for fixer in refactor.get_fixers_from_package(package + '.fixes')
                  # 'import' is done here (knows the files next to the file); 'future' is not needed
                  if not fixer.endswith(('.fix_import', '.fix_future'))]
        return refactor.RefactoringTool(fixers)
    return None


def siblings_of(names):
    """names of the modules in a directory, from a list of file names in that directory."""
    found = set()
    for name in names:
        if name.endswith('.py') and name != '__init__.py':
            found.add(name[:-3])
    return found


FROM_RE = re.compile(r'^([ \t]*)from[ \t]+([A-Za-z_][A-Za-z0-9_]*)([ \t]+import[ \t(*])', re.M)
IMPORT_RE = re.compile(
    r'^([ \t]*)import[ \t]+([A-Za-z_][A-Za-z0-9_]*)((?:[ \t]+as[ \t]+[A-Za-z_][A-Za-z0-9_]*)?[ \t]*(?:#[^\r\n]*)?)(?=\r?$)',
    re.M)


def explicit_relative_imports(text, siblings):
    """'from sibling import x' -> 'from .sibling import x'; 'import sibling' -> 'from . import sibling'."""
    count = [0]

    def from_sub(match):
        if match.group(2) in siblings:
            count[0] += 1
            return match.group(1) + 'from .' + match.group(2) + match.group(3)
        return match.group(0)

    def import_sub(match):
        if match.group(2) in siblings:
            count[0] += 1
            return match.group(1) + 'from . import ' + match.group(2) + match.group(3)
        return match.group(0)

    text = FROM_RE.sub(from_sub, text)
    text = IMPORT_RE.sub(import_sub, text)
    return text, count[0]


def compiles(text, name):
    """'' if text is valid python 3, else the error."""
    try:
        compile(text, name, 'exec', dont_inherit=True)
    except (SyntaxError, ValueError) as exc:
        return '%s: %s' % (exc.__class__.__name__, exc)
    return ''


def port_source(data, siblings, name, tool=None):
    """
    Port one python file. data: bytes.
    Returns (new data (bytes), list of what is done, error ('' if OK), list of (line number, line, why) to review)
    """
    # pylint: disable=too-many-branches
    done = []
    try:
        encoding = tokenize.detect_encoding(io.BytesIO(data).readline)[0]
        text = data.decode(encoding)
    except (SyntaxError, UnicodeDecodeError, LookupError):
        # python 2: no coding line and not ascii: bytes are passed as they are. Use latin-1, write as utf-8.
        encoding = 'utf-8'
        text = data.decode('latin-1')
        done.append('written as utf-8 (was not utf-8, without coding line)')
    if text.startswith('﻿'):
        text = text[1:]
    newline = '\r\n' if '\r\n' in text else '\n'

    text, count = explicit_relative_imports(text, siblings)
    if count:
        done.append('%s import(s) of a file next to it made explicit' % count)

    error = compiles(text, name)
    if error or PY2_HINTS.search(text):
        if tool is None:
            if error:
                return data, done, 'is python 2 (%s); to convert install python library "fissix"' % error, []
        else:
            try:
                converted = str(tool.refactor_string(text if text.endswith('\n') else text + '\n', name))
            except Exception as exc:  # pylint: disable=broad-exception-caught
                converted = None
                if error:
                    return data, done, 'can not be converted: %s' % exc, []
            if converted is not None and converted != text and not compiles(converted, name):
                if newline == '\r\n' and '\r\n' not in converted:
                    converted = converted.replace('\n', '\r\n')
                text = converted
                done.append('python 2 -> python 3')
            error = compiles(text, name)
    if error:
        return data, done, error, []

    review = []
    divisions = division_lines(text)
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if number in divisions:
            review.append((number, stripped[:160], DIVISION))
            continue
        for pattern, why in REVIEW:
            if pattern.search(line):
                review.append((number, stripped[:160], why))
                break
    try:
        newdata = text.encode(encoding)
    except UnicodeEncodeError:
        newdata = text.encode('utf-8')
    return (newdata if done else data), done, '', review


DIVISION = ('division: "/" of two whole numbers gives a whole number in python 2 (7/2 is 3) and a float in '
            'python 3 (3.5); use "//" where a whole number is needed (index, slice, range, counter)')


def division_lines(text):
    """Line numbers with a division that can be a division of whole numbers: not when one of the two sides is
    a number with a decimal point, or float(...) / Decimal(...)."""
    def is_float(node):
        if isinstance(node, ast.Constant):
            return isinstance(node.value, float)
        if isinstance(node, ast.Call):
            name = getattr(node.func, 'id', getattr(node.func, 'attr', ''))
            return name in ('float', 'Decimal')
        return False

    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return set()
    lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            if not is_float(node.left) and not is_float(node.right):
                lines.add(node.lineno)
        elif isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Div) and not is_float(node.value):
            lines.add(node.lineno)
    return lines


class Report:
    """what is done in a port; can be written as json and as text."""

    def __init__(self):
        self.files = 0          # all files
        self.python = 0         # python files
        self.changed = {}       # file: [what is done]
        self.errors = {}        # file: error
        self.review = {}        # file: [(line number, line, why)]
        self.skipped = []       # files not copied

    def add(self, name, done, error, review):
        self.python += 1
        if done:
            self.changed[name] = done
        if error:
            self.errors[name] = error
        if review:
            self.review[name] = review

    def as_dict(self):
        return {'files': self.files, 'python': self.python, 'changed': self.changed, 'errors': self.errors,
                'review': self.review, 'skipped': self.skipped}

    def summary(self):
        kinds = {}
        for done in self.changed.values():
            for what in done:
                what = re.sub(r'^\d+ ', '', what)
                kinds[what] = kinds.get(what, 0) + 1
        lines = ['%s files, %s python files' % (self.files, self.python),
                 '%s python files changed' % len(self.changed)]
        lines += ['    %s: %s files' % (what, count) for what, count in sorted(kinds.items())]
        lines.append('%s python files with an error (not valid python 3)' % len(self.errors))
        lines += ['    %s: %s' % item for item in sorted(self.errors.items())[:50]]
        lines.append('%s lines in %s files to review' % (
            sum(len(lines_) for lines_ in self.review.values()), len(self.review)))
        return '\n'.join(lines)


def modules_in(directory):
    """names of the python modules in a directory ([] if the directory is not there)."""
    if directory and os.path.isdir(directory):
        return siblings_of(os.listdir(directory))
    return set()


def port_tree(source, destination, report=None, tool=None, prefix='', target=None):
    """
    Port directory source to (new) directory destination. Returns Report.
    target: the directory the result will be put in later (eg usersys/grammars/edifact for a directory
    with edifact grammars): an import of a file that is in that directory is an import of a file next
    to it ('from edifact import syntax', where edifact.py is in the usersys and not in the source).
    """
    report = report or Report()
    tool = tool or refactoringtool()
    for dirpath, dirnames, filenames in os.walk(source):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        relative = os.path.relpath(dirpath, source)
        todir = os.path.normpath(os.path.join(destination, relative))
        os.makedirs(todir, exist_ok=True)
        siblings = siblings_of(filenames) | set(
            name for name in dirnames if os.path.isfile(os.path.join(dirpath, name, '__init__.py')))
        if target:
            siblings |= modules_in(os.path.join(target, relative))
        for filename in sorted(filenames):
            name = (prefix + os.path.join(relative, filename)).replace(os.sep, '/').replace('./', '', 1)
            if filename.endswith(('.pyc', '.pyo')):
                report.skipped.append(name)
                continue
            report.files += 1
            if not filename.endswith('.py'):
                shutil.copyfile(os.path.join(dirpath, filename), os.path.join(todir, filename))
                continue
            with open(os.path.join(dirpath, filename), 'rb') as pyfile:
                data = pyfile.read()
            if filename == 'botsindex.py' and relative == '.':
                # index of a plugin: is read by bots as data, also when written by python 2
                newdata, done, error, review = data, [], '', []
                report.python += 1
            else:
                newdata, done, error, review = port_source(data, siblings, name, tool)
                report.add(name, done, error, review)
            with open(os.path.join(todir, filename), 'wb') as pyfile:
                pyfile.write(newdata)
    return report


def port_zip(source, destination, report=None, tool=None, target=None):
    """
    Port a plugin or a zip with grammars. destination: a directory, or a name that ends with .zip
    target: see port_tree; for a zip with one directory in it (a grammar library) target is the place of
    the files in that directory.
    """
    report = report or Report()
    workdir = destination + '.unzipped' if destination.lower().endswith('.zip') else destination
    original = workdir + '.original'
    for directory in (original,) + ((workdir,) if workdir != destination else ()):
        shutil.rmtree(directory, ignore_errors=True)
    try:
        with zipfile.ZipFile(source) as archive:
            for info in archive.infolist():
                # no file outside the directory
                member = os.path.realpath(os.path.join(original, info.filename))
                if os.path.commonpath([os.path.realpath(original), member]) != os.path.realpath(original):
                    raise ValueError('"%s" in "%s" is not a file name that can be used.' % (info.filename, source))
            archive.extractall(original)
        tops = os.listdir(original)
        if target and len(tops) == 1 and os.path.isdir(os.path.join(original, tops[0])):
            # one directory with the files: these files go into target
            port_tree(os.path.join(original, tops[0]), os.path.join(workdir, tops[0]), report, tool,
                      prefix=tops[0] + '/', target=target)
        else:
            port_tree(original, workdir, report, tool, target=target)
        if workdir != destination:
            with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
                for dirpath, _dirnames, filenames in os.walk(workdir):
                    for filename in sorted(filenames):
                        full = os.path.join(dirpath, filename)
                        archive.write(full, os.path.relpath(full, workdir).replace(os.sep, '/'))
    finally:
        shutil.rmtree(original, ignore_errors=True)
        if workdir != destination:
            shutil.rmtree(workdir, ignore_errors=True)
    return report


def write_review(report, filename):
    with open(filename, 'w', encoding='utf-8') as out:
        out.write('Lines to review after porting to python 3\n=========================================\n')
        for name in sorted(report.review):
            out.write('\n%s\n' % name)
            for number, line, why in report.review[name]:
                out.write('  %5s: %s\n         -> %s\n' % (number, line, why))


def start():
    """bots-portusersys"""
    usage = """
    This is "%(name)s", part of Bots open source edi translator (https://bots-edi.org).
    Converts user scripts of bots 3 (python 2) to python 3. The source is not changed.

    Usage:
        %(name)s <source> <destination> [--target=<directory>] [--json=<file>] [--review=<file>]

        <source>        directory (a usersys, or a directory with grammars), or a zip-file (plugin, grammars).
        <destination>   directory that is made; for a zip-file as source this can be a zip-file.
        --target=<directory>  where the result will be put later, if the source is a part of a usersys.
                        Eg for a directory or zip with edifact grammars: <usersys>/grammars/edifact.
                        Needed when files import a file that is not in the source but in that directory
                        ('from edifact import syntax').
        --json=<file>   write all results as json.
        --review=<file> write the lines to review to this file (default: <destination>.review.txt).

    Exit code: 0 OK; 1 there are files that are not valid python 3; 2 error in the arguments.
    After this: put the result in the environment and run bots-checkusersys.
    """ % {'name': os.path.basename(sys.argv[0])}
    paths, jsonfile, reviewfile, target = [], None, None, None
    for arg in sys.argv[1:]:
        if arg.startswith('--json='):
            jsonfile = arg[7:]
        elif arg.startswith('--target='):
            target = arg[9:]
        elif arg.startswith('--review='):
            reviewfile = arg[9:]
        elif arg.startswith('-') or arg in ('?', '/?'):
            print(usage)
            sys.exit(0)
        else:
            paths.append(arg)
    if len(paths) != 2 or not os.path.exists(paths[0]):
        print(usage)
        print('Error: give a source that exists, and a destination.')
        sys.exit(2)
    source, destination = paths
    if os.path.exists(destination) and (not os.path.isdir(destination) or os.listdir(destination)):
        print('Error: destination "%s" exists (and is not an empty directory).' % destination)
        sys.exit(2)
    tool = refactoringtool()
    if tool is None:
        print('Warning: python library "fissix" is not installed: files with python 2 syntax are not converted.')
    if target and not os.path.isdir(target):
        print('Error: target "%s" is not a directory.' % target)
        sys.exit(2)
    report = port_zip(source, destination, tool=tool, target=target) if os.path.isfile(source) \
        else port_tree(source, destination, tool=tool, target=target)
    print(report.summary())
    if report.review:
        reviewfile = reviewfile or destination.rstrip('/\\') + '.review.txt'
        write_review(report, reviewfile)
        print('Lines to review are in: %s' % reviewfile)
    if jsonfile:
        with open(jsonfile, 'w', encoding='utf-8') as out:
            json.dump(report.as_dict(), out, indent=1)
    sys.exit(1 if report.errors else 0)


# *********************************************************************************************
# check the usersys of an environment
# *********************************************************************************************
SCRIPT_DIRS = ('mappings', 'routescripts', 'communicationscripts', 'envelopescripts', 'partners', 'charsets',
               'codeconversions', 'dbconnectors')
STRUCTURE = re.compile(r'^structure\s*=', re.M)
_INITIALISED = []


def _init(configdir):
    """in each process that checks: initialise bots once."""
    if not _INITIALISED:
        from . import botsglobal, botsinit  # pylint: disable=import-outside-toplevel
        botsinit.generalinit(configdir)
        import logging  # pylint: disable=import-outside-toplevel
        logger = logging.getLogger('bots.checkusersys')
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
        botsglobal.logger = logger
        _INITIALISED.append(True)


def _check_files(configdir, jobs):
    """
    jobs: list of (kind, editype or directory, name, path); kind: 'grammar', 'import'.
    Returns list of (kind, relative name, error) for what failed, and number checked.
    """
    # pylint: disable=import-outside-toplevel, broad-exception-caught
    _init(configdir)
    from . import botslib, grammar
    failed = []
    for kind, first, name, relative in jobs:
        try:
            if kind == 'grammar':
                grammar.grammarread(first, name, typeofgrammarfile='grammars')
            elif first:
                botslib.botsimport(*(first.split('/') + [name]))
            else:
                botslib.botsimport(name)
        except Exception as exc:
            text = str(exc).strip().splitlines()
            failed.append((kind, relative, '%s: %s' % (exc.__class__.__name__, text[-1][:300] if text else '')))
    return failed, len(jobs)


def usersys_jobs(usersys):
    """what to check in a usersys: (list of jobs, list of (file, error) that do not compile)."""
    jobs, notcompiled, pythonfiles = [], [], 0
    for dirpath, dirnames, filenames in os.walk(usersys):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        relative = os.path.relpath(dirpath, usersys).replace(os.sep, '/')
        parts = [] if relative == '.' else relative.split('/')
        for filename in sorted(filenames):
            if not filename.endswith('.py'):
                continue
            pythonfiles += 1
            name = '/'.join(parts + [filename])
            with open(os.path.join(dirpath, filename), 'rb') as pyfile:
                data = pyfile.read()
            try:
                compile(data, name, 'exec', dont_inherit=True)
            except (SyntaxError, ValueError) as exc:
                notcompiled.append((name, '%s: %s' % (exc.__class__.__name__, exc)))
                continue
            if filename == '__init__.py' or not parts:
                continue
            if parts[0] == 'grammars' and len(parts) == 2 and STRUCTURE.search(data.decode('utf-8', 'replace')):
                # a grammar with a structure: a message or an envelope
                jobs.append(('grammar', parts[1], filename[:-3], name))
            else:
                jobs.append(('import', '/'.join(parts), filename[:-3], name))
    return jobs, notcompiled, pythonfiles


def check_usersys(configdir=None, processes=1, progress=None):
    """
    Check the usersys of the environment of configdir.
    Returns dict: {'usersys':..., 'python': n, 'grammars': n, 'scripts': n,
                   'notcompiled': [(file, error)], 'failed': [(kind, file, error)]}
    """
    _init(configdir)
    from . import botsglobal  # pylint: disable=import-outside-toplevel
    usersys = botsglobal.ini.get('directories', 'usersysabs')
    configdir = botsglobal.ini.get('directories', 'config')
    jobs, notcompiled, pythonfiles = usersys_jobs(usersys)
    result = {'usersys': usersys, 'python': pythonfiles, 'notcompiled': notcompiled, 'failed': [],
              'grammars': sum(1 for job in jobs if job[0] == 'grammar'),
              'scripts': sum(1 for job in jobs if job[0] == 'import')}
    chunks = [jobs[start:start + 200] for start in range(0, len(jobs), 200)]
    done = 0
    if processes <= 1 or len(chunks) <= 1:
        for chunk in chunks:
            failed, count = _check_files(configdir, chunk)
            result['failed'] += failed
            done += count
            if progress:
                progress(done, len(jobs))
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as pool:
            for failed, count in pool.map(_check_files, [configdir] * len(chunks), chunks):
                result['failed'] += failed
                done += count
                if progress:
                    progress(done, len(jobs))
    result['failed'].sort()
    return result


def start_check():
    """bots-checkusersys"""
    usage = """
    This is "%(name)s", part of Bots open source edi translator (https://bots-edi.org).
    Checks the usersys of an environment: compiles every python file, reads every grammar (with the
    checks of a translation), imports every script (mappings, route scripts, etc).

    Usage:
        %(name)s [-c<directory>] [--processes=<number>] [--json=<file>]

        -c<directory>          directory for configuration files (default: config).
        --processes=<number>   check with this number of processes (default: 1).
        --json=<file>          write all results as json.

    Exit code: 0 no errors found; 1 errors found.
    """ % {'name': os.path.basename(sys.argv[0])}
    configdir, processes, jsonfile = None, 1, None
    for arg in sys.argv[1:]:
        if arg.startswith('-c') and not arg.startswith('--'):
            configdir = arg[2:]
        elif arg.startswith('--processes='):
            processes = int(arg[12:])
        elif arg.startswith('--json='):
            jsonfile = arg[7:]
        else:
            print(usage)
            sys.exit(0)

    def progress(done, total):
        print('\r%s of %s checked' % (done, total), end='', file=sys.stderr, flush=True)

    result = check_usersys(configdir, processes, progress)
    print('', file=sys.stderr)
    print('usersys: %s' % result['usersys'])
    print('%s python files; %s do not compile' % (result['python'], len(result['notcompiled'])))
    for name, error in result['notcompiled'][:100]:
        print('    %s: %s' % (name, error))
    for kind, label in (('grammar', 'grammars'), ('import', 'scripts')):
        failed = [item for item in result['failed'] if item[0] == kind]
        print('%s %s; %s with an error' % (result[label], label if kind == 'grammar' else 'other files', len(failed)))
        for _kind, name, error in failed[:100]:
            print('    %s: %s' % (name, error))
    if jsonfile:
        with open(jsonfile, 'w', encoding='utf-8') as out:
            json.dump(result, out, indent=1)
    sys.exit(1 if result['notcompiled'] or result['failed'] else 0)


if __name__ == '__main__':
    start()

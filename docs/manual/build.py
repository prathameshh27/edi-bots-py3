"""Builds the Bots manual: docs/manual/src/*.html (sections) -> docs/manual/site/ (one page per section, the menu
list and the search index). The look and the script are those of the Bots Studio knowledge base
(assets/kb.css, assets/manual.js), so the pages also work when opened straight from disk.

usage: python build.py            build, and report problems (exit code 1 if there are any)
"""
import html
import html.parser
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'src'
SITE = HERE / 'site'
UPDATED = '15 October 2026'

# the order of the manual (ids from BRIEF.md); 'welcome' becomes index.html
ORDER = [
    'welcome', 'how-bots-works', 'glossary', 'install-windows', 'install-linux', 'environments', 'first-start',
    'tutorial-first-route', 'tutorial-first-translation', 'upgrade-from-bots3',
    'int-overview', 'int-orders-in', 'int-orders-out', 'int-logistics', 'int-xml-hub', 'int-going-live',
    'routes', 'channels', 'channel-file', 'channel-ftp', 'channel-sftp', 'channel-mail', 'channel-database',
    'channel-other', 'partners', 'translations', 'confirm-rules', 'code-lists', 'counters',
    'grammars', 'grammar-syntax', 'grammar-records', 'editype-edifact', 'editype-x12', 'editype-csv-fixed',
    'editype-xml-json', 'editype-other', 'mappings', 'mapping-functions', 'mapping-recipes',
    'envelopes', 'acknowledgements', 'user-scripts', 'communication-scripts', 'route-scripts', 'envelope-scripts',
    'preprocessing',
    'bots-ini', 'settings-py', 'databases', 'command-line', 'scheduling', 'acceptance-testing', 'logging',
    'maintenance', 'security',
    'web-interface', 'web-reports', 'web-users', 'plugins',
    'troubleshooting', 'error-messages', 'faq',
]
VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'col', 'wbr', 'source', 'path', 'rect', 'circle', 'line',
        'polyline', 'polygon', 'ellipse', 'stop'}
FORBIDDEN = {'script', 'style', 'iframe', 'object', 'embed', 'form', 'html', 'head', 'body'}
SECTION = re.compile(r'<section\s+id="([^"]+)"\s+data-title="([^"]*)"\s+data-group="([^"]*)"\s*>(.*?)</section>',
                     re.S)

PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Bots manual</title>
<link rel="stylesheet" href="assets/kb.css">
</head>
<body data-updated="{updated}">
<main class="kb-main">
{content}
</main>
<script src="assets/pages.js"></script>
<script src="assets/search-index.js"></script>
<script src="assets/manual.js"></script>
</body>
</html>
'''


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:60] or 'part'


def page_file(section_id):
    return 'index.html' if section_id == 'welcome' else section_id + '.html'


class Checker(html.parser.HTMLParser):
    """tag balance, forbidden tags; collects ids and links"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.problems, self.ids, self.links = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in FORBIDDEN:
            self.problems.append('tag <%s> is not allowed' % tag)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.problems.append('</%s> without an opening tag' % tag)
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for t, line in self.stack[i + 1:]:
                    self.problems.append('<%s> (line %d) is not closed' % (t, line))
                del self.stack[i:]
                return
        self.problems.append('</%s> without an opening tag' % tag)


class TextIndex(html.parser.HTMLParser):
    """search entries: one per h1/h2/h3 part of a page"""

    def __init__(self, file, page):
        super().__init__(convert_charrefs=True)
        self.file, self.page, self.entries = file, page, []
        self.heading, self.anchor, self.text, self.in_head, self.head_text = page, '', [], None, []
        self.skip = 0

    def flush(self):
        text = re.sub(r'\s+', ' ', ' '.join(self.text)).strip()
        if text or self.heading:
            self.entries.append({'file': self.file, 'page': self.page, 'heading': self.heading,
                                 'anchor': self.anchor, 'text': text[:4000]})
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in ('h1', 'h2', 'h3'):
            self.flush()
            self.in_head, self.head_text = tag, []
            self.anchor = dict(attrs).get('id', '') if tag != 'h1' else ''
        if tag == 'svg':
            self.skip += 1

    def handle_endtag(self, tag):
        if tag == self.in_head:
            self.heading = re.sub(r'\s+', ' ', ''.join(self.head_text)).strip()
            self.in_head = None
        if tag == 'svg':
            self.skip -= 1

    def handle_data(self, data):
        if self.skip:
            return
        (self.head_text if self.in_head else self.text).append(data)

    def close(self):
        super().close()
        self.flush()


def shift_headings(content, section_id):
    """h2 -> h1 (the page title), h3 -> h2, h4 -> h3; every h2/h3 gets an id for 'On this page' and search"""
    content = re.sub(r'<(/?)h2\b', r'<\1h1', content)
    content = re.sub(r'<(/?)h3\b', r'<\1h2', content)
    content = re.sub(r'<(/?)h4\b', r'<\1h3', content)
    used = set(re.findall(r'\bid="([^"]+)"', content))

    def add_id(match):
        tag, attrs, inner = match.group(1), match.group(2), match.group(3)
        if 'id=' in attrs:
            return match.group(0)
        base = '%s--%s' % (section_id, slug(re.sub(r'<[^>]+>', '', inner)))
        anchor, n = base, 2
        while anchor in used:
            anchor, n = '%s-%d' % (base, n), n + 1
        used.add(anchor)
        return '<%s id="%s"%s>%s</%s>' % (tag, anchor, attrs, inner, tag)
    return re.sub(r'<(h2|h3)((?:\s[^>]*)?)>(.*?)</\1>', add_id, content, flags=re.S)


def main():
    problems = []
    sections = {}
    for path in sorted(SRC.glob('*.html')):
        text = path.read_text(encoding='utf8')
        found = SECTION.findall(text)
        if not found:
            problems.append('%s: no <section id=... data-title=... data-group=...>' % path.name)
        for section_id, title, group, content in found:
            if section_id in sections:
                problems.append('%s: section "%s" is written twice' % (path.name, section_id))
            sections[section_id] = dict(title=html.unescape(title), group=html.unescape(group),
                                        content=content.strip(), source=path.name)
    missing = [s for s in ORDER if s not in sections]
    extra = [s for s in sections if s not in ORDER]
    problems += ['section "%s" is missing' % s for s in missing]
    problems += ['section "%s" is not in the order of the manual' % s for s in extra]
    order = [s for s in ORDER if s in sections] + extra

    # every id -> the page it is on
    pages, where = [], {}
    for section_id in order:
        s = sections[section_id]
        s['content'] = shift_headings(s['content'], section_id)
        s['file'] = page_file(section_id)
        where[section_id] = s['file']
        for anchor in re.findall(r'\bid="([^"]+)"', s['content']):
            if anchor in where and where[anchor] != s['file']:
                problems.append('id "%s" is used on two pages (%s, %s)' % (anchor, where[anchor], s['file']))
            where.setdefault(anchor, s['file'])
        pages.append({'group': s['group'], 'file': s['file'], 'title': s['title']})

    def link(match, own_file):
        target = match.group(1)
        if target in sections:
            return 'href="%s"' % where[target]
        if target in where:
            return 'href="%s#%s"' % ('' if where[target] == own_file else where[target], target)
        problems.append('%s: link to "#%s", which does not exist' % (own_file, target))
        return match.group(0)

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / 'assets').mkdir(parents=True)
    index = []
    for section_id in order:
        s = sections[section_id]
        content = re.sub(r'href="#([^"]+)"', lambda m, f=s['file']: link(m, f), s['content'])
        checker = Checker()
        checker.feed(content)
        checker.close()
        problems += ['%s (%s): %s' % (s['file'], s['source'], p) for p in checker.problems]
        problems += ['%s: <%s> (line %d) is not closed' % (s['file'], t, line) for t, line in checker.stack]
        (SITE / s['file']).write_text(PAGE.format(title=html.escape(s['title']), updated=UPDATED, content=content),
                                      encoding='utf8', newline='\n')
        indexer = TextIndex(s['file'], s['title'])
        indexer.feed(content)
        indexer.close()
        index += indexer.entries

    for name in ('kb.css', 'manual.js'):
        shutil.copyfile(HERE / 'assets' / name, SITE / 'assets' / name)
    (SITE / 'assets' / 'pages.js').write_text(
        '// Written by docs/manual/build.py. Do not edit by hand.\nwindow.MANUAL_PAGES = '
        + json.dumps(pages, ensure_ascii=False, indent=1) + ';\n', encoding='utf8', newline='\n')
    (SITE / 'assets' / 'search-index.js').write_text(
        '// Written by docs/manual/build.py. Do not edit by hand.\nwindow.KB_INDEX = '
        + json.dumps(index, ensure_ascii=False) + ';\n', encoding='utf8', newline='\n')

    words = sum(len(re.sub(r'<[^>]+>', ' ', sections[s]['content']).split()) for s in order)
    print('%d pages, %d search entries, about %d words -> %s' % (len(order), len(index), words, SITE))
    for p in problems:
        print('PROBLEM:', p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())

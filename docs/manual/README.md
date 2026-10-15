# The Bots manual

The user manual of Bots EDI Translator 4.0: how-to guides, every setting, integration tutorials and
troubleshooting for every topic. It is a static HTML site: one page per topic, a menu, an "on this page" list,
search, and a light and a dark theme. It needs no web server and no internet connection.

## Reading it

Build it once (see below), then open `site/index.html` in a browser.

## What is in this folder

| Path | What it is |
|---|---|
| `src/*.html` | The text of the manual. Each file holds one or more `<section>`s; every section becomes one page |
| `assets/kb.css` | The look of the pages |
| `assets/manual.js` | Builds the menu, the "on this page" list, the search box and the theme switch in the browser |
| `build.py` | Makes `site/` from `src/` and `assets/` |
| `BRIEF.md` | The writing guide: audience, structure of a page, building blocks, style, the list of sections |
| `site/` | The built manual (made by `build.py`; not in version control) |

The files in `src/` are numbered only to keep them in order on disk. The order of the pages in the manual is the
list `ORDER` in `build.py`.

## Building

```bash
python build.py
```

It needs only Python 3 (no packages). It writes one page per section to `site/`, plus `site/assets/pages.js`
(the menu) and `site/assets/search-index.js` (the search). It then reports problems and exits with code 1 if
there are any:

- a section in `ORDER` that is missing, or a section that is not in `ORDER`
- a link to a section or anchor that does not exist
- a tag that is not closed, or a tag that is not allowed (`script`, `style`, `iframe`, ...)
- the same id on two pages

A clean build prints one line, for example `63 pages, 840 search entries, about 169000 words -> .../site`.

## Changing a page

1. Find the section: `grep -l 'id="routes"' src/*.html`.
2. Edit the HTML between its `<section …>` and `</section>`.
3. Run `python build.py` and look at the page in `site/`.

Links between pages are written as `<a href="#section-id">` (or `#section-id--anchor`); `build.py` turns them
into links to the right page.

## Adding a page

1. Write a section in a file in `src/` (a new file or an existing one):
   ```html
   <section id="my-topic" data-title="My topic" data-group="Configure">
   <h2>My topic</h2>
   <p class="lead">What this is and when you need it.</p>
   <div class="note plain"><span class="label">In plain words</span><p>…</p></div>
   …
   </section>
   ```
2. Add `'my-topic'` to `ORDER` in `build.py`, at the place where it belongs.
3. Run `python build.py`.

The group (`data-group`) is the heading the page appears under in the menu.

## Rules for the content

`BRIEF.md` has them in full. In short:

- **Only what Bots 4 has.** Describe the program as the code behaves; when the code and an older description
  differ, the code wins. Do not describe features Bots 4 does not have.
- **Generic names only.** Examples use the invented cast of `BRIEF.md` (MyCompany, PartnerA, PartnerB,
  PartnerC, hosts under `example.com`, ...) and invented data. Never a real company, person, server, file or
  value.
- **Every page has the same parts:** a lead, an "In plain words" box, how it works, how-to steps, a reference
  of every setting, and a troubleshooting table (what you see, why, fix) with the real error texts of Bots.
- **Tutorials are run before they are written:** the files and outputs on a tutorial page are those of a real
  run.
- **Building blocks:** `note plain/info/tip/warn/stop`, `span.ui` for screen and button names, `ol.steps`,
  `table.fix` for troubleshooting, badges (`new in 4.0`, `advanced`, ...), inline SVG diagrams (no external
  scripts or pictures, so the manual works offline).

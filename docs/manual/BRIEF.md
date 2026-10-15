# Brief for the writers of the Bots manual

## UPDATE (applies over everything below): the format of the Bots Studio knowledge base

The owner already has a knowledge base for Bots Studio (a front end on Bots) and the Bots manual must look and
work like it: same building blocks, same classes. Write your sections with these, instead of the callouts,
`dl.trouble` and mermaid described further down:

- Start every section, right after the lead paragraph, with an "In plain words" box:
  `<div class="note plain"><span class="label">In plain words</span><p>…everyday explanation, no jargon…</p></div>`
- Callouts: `<div class="note info">`, `<div class="note tip">`, `<div class="note warn">` (something can go
  wrong), `<div class="note stop">` (you can lose data, or it is not allowed); each starts with
  `<span class="label">Note</span>` / `Tip` / `Watch out` / `Stop` and then `<p>`.
- Names of screens, menus, buttons and fields of the web interface: `<span class="ui">Channels</span>`; a menu
  path as `<span class="ui">Configuration</span> → <span class="ui">Channels</span> → <span class="ui">Add</span>`.
- Task steps: `<ol class="steps">`, each `<li>` starting with the action in `<b>…</b>`.
- Every table inside `<div class="table-wrap">…</div>`; reference tables `<table>` with a header row.
- Troubleshooting: one or more tables in the knowledge base's form:
  `<div class="table-wrap"><table class="fix"><tr><th>What you see</th><th>Why</th><th>Fix</th></tr>…</table></div>`;
  "What you see" is the symptom or the exact message text. At least 5 rows per section, more for big topics.
- Badges: `<span class="badge green">new in 4.0</span>`, `<span class="badge gray">advanced</span>`,
  `<span class="badge orange">changed in 4.0</span>`, `<span class="badge red">removed</span>`.
- Diagrams: no mermaid (the manual must work offline). Use a small inline SVG in `<div class="diagram">`, in
  this pattern (boxes `class="box in"` for receiving, `box mid` for processing, `box out` for sending; text
  `class="small"` for the second line; arrows `class="arrow"`; give each marker a unique id per diagram, eg
  `arrow-routes-1`):
  ```html
  <div class="diagram"><svg viewBox="0 0 760 150" width="760" role="img" aria-label="…">
  <defs><marker id="arrow-x-1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>
  <rect class="box in" x="10" y="30" width="200" height="80" rx="10"/><text x="110" y="64" text-anchor="middle" font-weight="600">1. Receive</text><text class="small" x="110" y="86" text-anchor="middle">second line</text>
  <path class="arrow" d="M214,70 L276,70" marker-end="url(#arrow-x-1)"/>
  …</svg></div>
  ```
  Use diagrams where they really help; a numbered list is fine elsewhere.
- Use `<b>` for emphasis of key words (as the knowledge base does), `<code>` for code, file names, settings.
- Keep `<section id=… data-title=… data-group=…>` exactly as below: each section becomes one page.

You write one part of **The Bots Manual**: a complete user manual of Bots EDI Translator, version 4.0.0 (the
Python 3 version in this repository, `bots-new-stable`). It is one HTML file in the end; you write HTML fragments
that are put together by `docs/manual/build.py`.

## Who reads it

A newcomer to EDI and to Bots: knows how to use a computer and a text editor, maybe a little Python, nothing
about EDI. After reading, they can install Bots, set up partners, channels, routes, grammars and mappings, run
it in production and fix problems. Also the experienced user who looks up one setting.

## Sources (only these)

1. **The program itself** (the truth for version 4.0.0): `bots-new-stable/bots/**` — `models.py` (every field
   and choice of the web interface), `install/bots.ini` and `install/settings.py` (every setting, with comments),
   `grammar.py` (grammar syntax and defaults per editype), `transform.py` and `node.py` (mapping functions),
   `communication.py` (channel types, user script hooks), `router.py`, `engine.py`, `envelope.py`,
   `inmessage.py`, `outmessage.py`, `preprocess.py`, `botsinit.py`, `dbconnect.py`, `admin.py`, `views.py`,
   `urls.py`, `templates/**`, the command line tools (`[project.scripts]` in `pyproject.toml`, and their
   `start()` functions with their help texts), `bots/usersys/**` (examples that ship with Bots),
   `MIGRATION.md`, `CHANGELOG.rst`, `README.rst`.
2. **The official documentation**: https://bots.readthedocs.io/en/latest/ (written for Bots 3; use it for
   structure, concepts and explanations, but when it differs from the code, the code wins, and say what is new
   or different in 4.0.0).

Do **not** open, read or search anything else on this machine: not `.temp`, not `reports`, not `bots-old`,
not `bots-new`, not `bots-3.2.0`, not any `usersys` outside `bots-new-stable/bots/usersys`, not the user's home
folder. They contain private data of a real company.

## Names and examples: generic only

Every example uses invented, generic names. Use this cast so the whole manual is consistent:

| Thing | Name to use |
|---|---|
| Your own company | `MyCompany`, EDI id `MYCOMPANY` (X12: `ZZ` / `MYCOMPANY`; EDIFACT: `5412345000013` with qualifier `14`) |
| Partners | `PartnerA` (a retailer, sends orders, id `PARTNERA`), `PartnerB` (a supplier, id `PARTNERB`), `PartnerC` (a logistics company, id `PARTNERC`) |
| Partner group | `Retailers` |
| Hosts | `ftp.example.com`, `sftp.example.net`, `mail.example.org`, `db.example.com` (reserved example domains only) |
| Mail | `edi@mycompany.example`, `orders@partnera.example` |
| Users | `admin`, `operator`, `viewer` |
| Routes | `orders_in`, `invoices_out`, `asn_out`, `acks_in` |
| Channels | `partnera_sftp_in`, `partnera_sftp_out`, `local_orders_in`, `erp_invoices_out`, `mail_in`, `erp_db_in` |
| Files and folders | `botssys/infile/orders/`, `botssys/outfile/invoices/`, `C:\edi\in`, `/srv/edi/in` |
| Messages | X12 850 / 810 / 856 / 997, EDIFACT ORDERS / INVOIC / DESADV / CONTRL, csv, fixed, xml, json |
| Mapping and grammar names | `orders_x12_to_csv.py`, `invoice_csv_to_edifact.py`, `850004010.py` (standard), `orders_erp.py` |
| Passwords | `********` or `secret-example`; never anything that looks real |

Never invent a name that looks like a real company, person, product or server.

## Form of every section

Each section (`<section>`) is one "page" of the manual. Inside it, in this order, with these exact headings
where they apply:

1. `<h2>` the title, then a short lead paragraph `<p class="lead">`: what this is and when you need it, in
   two or three plain sentences.
2. **"How it works"** (`<h3>`): the concept, plainly, with a small diagram where it helps
   (`<pre class="mermaid">` with a mermaid flowchart, kept small) or a numbered list of steps.
3. **"How to …"** (`<h3>`, one or more): task guides. Numbered steps (`<ol class="steps">`), each step one
   action, saying exactly where to click in the web interface (menu path in `<span class="path">Configuration
   › Channels › Add</span>`) or what to type. Show the result to expect.
4. **"Reference"** (`<h3>`): every setting/field/option of the topic, in a table `<table class="ref">` with
   columns Name | What it does | Default | Values / example. Nothing tweakable may be left out: go through the
   code and list all of it (also the rarely used and the advanced ones; mark those `<span class="badge
   adv">advanced</span>`). Mark things new in 4.0.0 with `<span class="badge new">new in 4.0</span>`.
5. **"Troubleshooting"** (`<h3>`): a `<dl class="trouble">` of problems: `<dt>` the symptom as the user sees
   it (the error text where there is one), `<dd>` the cause and the fix in numbered steps. At least 5 real
   problems per section, more for the big topics. Take error texts from the code (`raise ...Error(_('...'))`)
   so they match what users see.

## Writing style

- Plain, short sentences. Active voice. Explain every EDI or Bots term the first time you use it in a section,
  or link it to the glossary: `<a href="#glossary">` … `</a>`.
- Second person ("you"). No marketing words, no "simply", no "just", no jokes, no emoji.
- Code, file names, settings and commands in `<code>`. Multi-line code in `<pre><code class="language-python">`
  (or `language-ini`, `language-bash`, `language-powershell`, `language-xml`, `language-json`, `language-text`).
- Callouts: `<div class="note">`, `<div class="tip">`, `<div class="warn">` (each starting with `<strong>Note</strong>`,
  `<strong>Tip</strong>`, `<strong>Warning</strong>`).
- Links between sections: `<a href="#section-id">`. Only link to ids that exist (the list is below).
- Windows and Linux both: give both commands where they differ.
- Be exact. If you are not sure how something behaves, read the code until you are. Do not describe features
  that are not in the code.

## HTML rules

- Write fragments only: no `<html>`, `<head>`, `<body>`, no `<style>`, no `<script>`.
- Each section: `<section id="the-id" data-title="Short title" data-group="Group name">` … `</section>`, with the
  id and group given to you. You may add `<h3 id="the-id--sub">` anchors for subsections (prefix with the
  section id and `--`).
- Allowed tags: section, h2, h3, h4, p, ul, ol, li, table, thead, tbody, tr, th, td, pre, code, kbd, strong, em,
  a, div (only with class note/tip/warn/example), span (class path/badge), dl, dt, dd, br, figure,
  figcaption. Escape `<`, `>`, `&` inside code.
- Valid, closed HTML. UTF-8.

## Sections and ids (the whole manual; write only yours)

Group **Start here**: `welcome` (What Bots is, how to use this manual), `how-bots-works` (a run, step by step),
`glossary`, `install-windows`, `install-linux`, `environments` (config/usersys/botssys, several environments,
BOTS_CONFIG_DIR), `first-start` (web server, first login, users), `tutorial-first-route`,
`tutorial-first-translation`, `upgrade-from-bots3`.

Group **Integration tutorials**: `int-overview` (planning an integration), `int-orders-in`, `int-orders-out`,
`int-logistics`, `int-xml-hub`, `int-going-live`.

Group **Configure**: `routes`, `channels`, `channel-file`, `channel-ftp`, `channel-sftp`, `channel-mail`,
`channel-database`, `channel-other` (mimefile, trash, communicationscript, http and any other type in the code),
`partners`, `translations`, `confirm-rules`, `code-lists`, `counters`.

Group **Grammars and mappings**: `grammars`, `grammar-syntax` (every syntax option per editype),
`grammar-records` (records, fields, formats, structure, nextmessage), `editype-edifact`, `editype-x12`,
`editype-csv-fixed`, `editype-xml-json`, `editype-other` (tradacoms, idoc, excel, templatehtml, raw, any other
editype in the code), `mappings`, `mapping-functions` (every transform function), `mapping-recipes`.

Group **Envelopes, acknowledgements, scripts**: `envelopes`, `acknowledgements` (997/999, CONTRL, MDN,
confirm), `user-scripts` (overview), `communication-scripts`, `route-scripts`, `envelope-scripts`,
`preprocessing` (mailbag and other preprocess functions).

Group **Run and maintain**: `bots-ini` (every setting of every section), `settings-py`, `databases` (SQLite,
MySQL/MariaDB, PostgreSQL, SQL Server for Bots itself), `command-line` (every command and option),
`scheduling` (cron, Windows tasks, job queue, directory monitor), `acceptance-testing`, `logging`,
`maintenance` (cleanup, backups, upgrades), `security`.

Group **Web interface**: `web-interface` (every screen and button), `web-reports` (incoming, outgoing,
process errors, document view, confirm, reports), `web-users` (users, groups, rights), `plugins`.

Group **Troubleshooting**: `troubleshooting` (the method: where to look first), `error-messages` (every error
message of Bots with its meaning and fix), `faq`.

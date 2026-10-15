Bots EDI Translator 4
=====================

Bots is complete, open source software for EDI (Electronic Data Interchange): it receives business documents
from your partners, translates them, and sends the results where they belong. Orders, invoices, ship notices,
acknowledgements and any other document, in EDIFACT, X12, TRADACOMS, XML, JSON, CSV, fixed-length files, IDoc,
Excel and more, over files, FTP, FTPS, SFTP, mail (POP3, IMAP, SMTP), HTTP and databases.

Bots 4 runs on Python 3 and Django. It is a drop-in successor of Bots 3: existing configurations, mappings,
grammars and plugins move over with the tools that come with it, and the regression suite checks that it
translates exactly as Bots 3.2.0 does.

What is new in Bots 4.0
-----------------------

Bots 4.0 builds on the Python 3 port of Bots (bots-ediint 4.0.0rc4) and makes it ready for production use.
Every change is described in `CHANGELOG.rst`_.

- **Bots 3 behaviour restored** wherever the Python 3 port differed. Checked with the 42 official plugins
  against stored results of Bots 3.2.0, and file by file against a production installation of nine
  environments.
- **Databases**: database channels for MySQL/MariaDB, PostgreSQL, SQLite and Microsoft SQL Server, with
  commit and rollback handled by Bots. Bots' own database can be any of the four, with the same output as
  SQLite.
- **Channels**: fixes for FTPS uploads, SFTP, finding partners by mail address, the XML mailbag, and data
  stored by Bots 3 on Python 2.
- **Moving from Bots 3**: ``bots-portenv`` makes a complete new environment from a Bots 3 one;
  ``bots-portusersys``, ``bots-checkusersys``, ``bots-portconfig`` and ``bots-updatedb`` do the separate
  steps. Step by step in `MIGRATION.md`_.
- **Your own look**: title, support link, logo and favicon of the web interface are settings.
- **Safe testing**: a local test mode keeps every channel of a test environment on local folders.
- **Tests**: unit tests, a regression suite with the official plugins, and a database test matrix, run by
  the GitHub workflow on every push.
- **The manual**: a complete user manual with how-to guides, every setting, integration tutorials and
  troubleshooting for every topic (see Documentation below).

Getting started
---------------

Bots 4 needs Python 3.10 or newer (3.12 or newer for Django 6).

.. code-block:: bash

    git clone https://github.com/prathameshh27/edi-bots-py3.git
    cd edi-bots-py3
    git checkout bots4
    python -m venv .venv
    source .venv/bin/activate       # Windows: .venv\Scripts\activate
    pip install ".[sftp]"           # add extras as needed, see below

    bots-webserver                  # then open http://localhost:8080

The first start makes an environment in ``~/.bots/env/default`` (configuration, your grammars and mappings,
and the data). Log in with user ``bots`` and password ``botsbots``, and change that password at once. Runs are started with
``bots-engine`` (by hand, from the web interface, or from a scheduler).

Optional parts are installed as extras, for example ``pip install ".[sftp,mysql]"``:

=================  ==========================================================
Extra              For
=================  ==========================================================
``sftp``           SFTP channels
``mysql``          MySQL / MariaDB (channels and Bots' own database)
``postgresql``     PostgreSQL
``mssql``          Microsoft SQL Server
``http``           HTTP(S) channels
``excel``          Excel files
``pdf``            PDF text extraction
``templatehtml``   HTML documents made from templates
``port``           Converting Python 2 scripts of Bots 3 (``bots-portusersys``)
``bots3``          Everything a typical Bots 3 installation used, to move it at once
``tools``          The optional libraries together (templates, SFTP, PDF, Excel)
``testing``        Running the tests
=================  ==========================================================

Documentation
-------------

The manual is in this repository, in `docs/manual`_. Build it once and open it in a browser; it needs no web
server and no internet connection:

.. code-block:: bash

    python docs/manual/build.py
    # then open docs/manual/site/index.html

It covers installing, how Bots works, every channel, grammar, mapping function and setting, the web
interface, running in production, every error message, and step-by-step tutorials from a first route to
complete integrations (orders in, acknowledgements, ship notices and invoices out, logistics with JSON, an
XML hub).

Also in this repository: `MIGRATION.md`_ (moving from Bots 3) and `CHANGELOG.rst`_ (every change).

Running the tests
-----------------

.. code-block:: bash

    pip install ".[testing,tools]"
    python -m pytest tests/unit tests/regression -n 4

Credits
-------

- **Henk-Jan Ebbers** created Bots and led it for many years (`bots.sourceforge.net`_). Bots exists because
  of his work.
- **The bots-ediint developers**, led by **Ludovic Watteaux**, with Wojtek Kazimierczak, Tom Westrick, Jared
  Miller and others, ported Bots to Python 3 and Django (`gitlab.com/bots-ediint/bots`_). Bots 4 starts from
  their version 4.0.0rc4.
- **Prathamesh Pavnoji** made Bots 4.0: the stabilisation for production use, the database support, the
  migration tools, the test suites and the manual.
- Everyone else who contributed over the years: see `AUTHORS.rst`_.

Commercial support
------------------

For help with installing, migrating from Bots 3, building integrations, or support for Bots 4 in production:

- **Prathamesh Pavnoji**
- E-mail: prathameshh27@gmail.com
- LinkedIn: https://www.linkedin.com/in/prathamesh-pavnoji/

License
-------

Bots is licensed under the GNU General Public License, version 3: see `license.rst`_ and
https://www.gnu.org/licenses/gpl-3.0.html.

.. _CHANGELOG.rst: CHANGELOG.rst
.. _MIGRATION.md: MIGRATION.md
.. _docs/manual: docs/manual
.. _AUTHORS.rst: AUTHORS.rst
.. _license.rst: license.rst
.. _bots.sourceforge.net: https://bots.sourceforge.net/en/index.shtml
.. _gitlab.com/bots-ediint/bots: https://gitlab.com/bots-ediint/bots

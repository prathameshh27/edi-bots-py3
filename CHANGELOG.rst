Bots - CHANGELOG
================


4.0.0 (unreleased)
------------------

Based on 4.0.0rc4 below.

What is compared with: "bots 3.2.0" is the release (github eppye-bots/bots, branch ``bots32``; the same as the
installers on sourceforge). The first rounds of this work compared with the ``master`` branch of that
repository, which is later development that was never released. Where that made a difference it is said below.
The reference of the regression tests is made with the release.

- x12 997: the IDs in the 997 and the IDs the confirm rules are checked with are GS02/GS03 of the received
  group, as in 3.2.0. 4.0 used the IDs found by the QUERIES of the envelope grammar (mostly ISA06/ISA08): another
  997, and 997's for one partner were not merged into one interchange. (An earlier change here was made to match
  ``master``.) With this the official x12 plugins give exactly the output that is shipped in the plugins.
- ``botslib.opendata()`` / ``readdata()`` without charset: the content is read and written as it is (each byte
  one character, no conversion of line ends), as in bots 3. A route script that reads a file with
  ``readdata()`` and writes it with ``opendata(name, 'wb')`` works again; in 4.0 that gave ``TypeError: a
  bytes-like object is required``, and the encoding and the line ends depended on the platform.
- xmlnocheck: a record without the internal ``BOTSIDnr`` (made or changed by a mapping itself) can be written
  again.

Errors that came with the code of bots 3, found by reading the code (each has a test in
``tests/unit/test_engine_errors.py`` or ``tests/regression/test_engine_run_errors.py``):

- A file that can not be read at all (an unknown editype) is an error of that file. The error handler used the
  edi file that was never made (``NameError``): the rest of the route's files were skipped in that run.
- An error while enveloping one message (the copy of its record fails) is put on that message. It went to the
  file of the message before it, or the handler itself failed.
- Messages to merge with an empty value (NULL) in one of the columns they are grouped by (editype, messagetype,
  testindicator, envelope, rsrv3, charset) are merged. They matched nothing, stayed TRANSLATED, and only the log
  said so.
- A user script whose own import fails (a library that is not installed) is reported as an error in that
  script. It counted as "no script": for a communication script bots' own channel class ran instead, without a
  word, and the failure was remembered for the rest of the run.
- An error in the set-up of a run itself (crash recovery, automatic retry, resend, rereceive) makes the run end
  with "errors in the run" (exit code 2). It was counted as no error: exit code 0, no report, no error mail.
- A received file that can not be removed from its folder (locked, no rights) is an error of the channel; the
  files after it are still received (it is received again in the next run). The first such file ended the
  channel. The same for communication scripts that receive files.
- Sending or receiving that fails still disconnects: the lock file of the channel is removed and the next run is
  not blocked.
- A failing database statement in ``query()`` and ``insertta()`` is rolled back (PostgreSQL refused every later
  statement), and the cursor is closed in all three statement functions.
- A new counter given a value (``unique(name, updatewith=...)``) stores that value. It stored 1: automatic retry
  of communication did nothing in its first two runs, and the daily clean-up ran twice on the first day.
- ``unique_runcounter`` (acceptance tests) starts again at 0 after the largest number, as ``unique`` does.
- Confirm rules read twice in one process are not doubled.
- The stack of processes stays right when recording the end of a process fails (later records had the wrong
  process and the wrong start of the run).
- Channel debugging (``LoggerPipe``) writes to the engine's logger; its default was the logger that existed when
  the module was imported.
- xmlrpc: the address has a ``:`` between user name and password. A password written as ``:password`` (the way
  that worked in bots 3) still works.
- The password of a channel is not shown in the web interface. The form had it as text, so whoever could change
  (or only view) a channel could read it, and the list showed as many stars as it had characters. Now the form
  field stays empty (left empty, the channel keeps its password; "Remove the password" removes it), and the list
  and the read-only view show ``********``. Tests in ``tests/unit/test_web_security.py``.

Carried over from the 3.2.0 release and from a patched bots 3 installation (a 3.2.0 release candidate with
local changes, compared file by file with the release):

- The partner of a mail address is also searched in the CC field of the partners, as 3.2.0 does (neither
  ``master`` nor 4.0 did). An address has to be equal to one of the addresses in the field: 3.2.0 also accepted
  a part of an address. New: also found when a partner has more than one address in its mail field.
- ``transform.persist_lookup()`` reads values written by bots 3 (python 2). A stored text with non-ASCII
  characters or a date/time raised ``UnicodeDecodeError`` in 4.0.
- Incoming editype ``mailbag`` at the parser: the file is read as xml (messagetype ``mailbag``: found via
  ``grammars/xml/mailbag.py``). 4.0 gave "Unknown editype for incoming message: mailbag". The normal way (a
  route with editype ``mailbag``, the mailbag step recognises xml) worked and now has tests, also for a route in
  parts (receive / translate / send).
- ``bots-portusersys`` lists divisions for review: ``len(x)/2`` is a whole number in python 2 and a float in
  python 3, where a slice or ``range()`` with it fails. 2to3 does not change these.
- xml, xmlnocheck: the attributes of an element are written in alphabetical order again, as bots 3 did and as
  the code says. Python 2 sorted them; since python 3.8 they came in the order of the puts in the mapping
  (seen in the production replay: 22 of 29 xml files differed in nothing else).
- An object of a database channel that bots 3 (python 2) received and stored is read: dates, decimals and
  non-ASCII byte strings in such a pickle gave "[A59]: incoming file has not allowed characters". Matters for
  files that are received but not translated at the moment of the move, and for re-processing the history
  (production replay: 386 of 450 stored objects of one environment). ``botslib.loads_pickled()``; persist
  uses the same.
- ftps, ftpis: sending a file no longer depends on the server closing TLS on the data connection. With a
  server that does not (seen with a public ftp service; the same with bots 3 on python 2.7) every upload
  above a few hundred bytes waited for the time-out and failed, and the next files failed on the answers of
  the server being out of step. Bots now waits at most 2 seconds for it.
- sftp: a file that is not on the server yet is opened for writing, not for append. To append the ssh library
  asks for the size of the file; a server that gives none for a new file got files of 0 bytes and
  ``TypeError: int() argument ... NoneType`` (the same with bots 3).
- Channels of type ``db``: new field "Database" (MySQL/MariaDB, PostgreSQL, SQLite, Microsoft SQL Server). When it is
  set bots makes the connection (host, port, username, password; database from "path", or "filename" as the
  scripts of bots 3 used; driver options from "parameters"); the communication script only needs
  ``incommunicate`` / ``outcommunicate``; bots commits when they end without error and rolls back otherwise.
  The connection behaves the same for every database: ``%(name)s`` or ``%s`` parameters, rows as dicts that can
  also be used by position (``bots.dbconnect``). A script with its own ``connect``/``disconnect`` works as in
  bots 3. Migration ``0007``.
- Database of bots itself on Microsoft SQL Server (django backend ``mssql-django``): table definitions for the
  engine tables, and bots-engine connects through ``bots.dbconnect`` (``merge``, a reserved word in SQL Server,
  is quoted). Install option ``[mssql]``. (Tests on a server: see ``tests/servers.py``.)
- Tests can run on a database server: ``BOTS_TEST_DATABASE=<kind>://<user>:<password>@<host>:<port>`` gives
  every test environment its own new database there (dropped afterwards); ``BOTS_TEST_CHANNEL_DATABASE`` only
  for the database of the channels.
- ``bots.ini [settings] channels_use_testpath = True``: every channel uses its testpath (ftp, sftp, mail, database
  become folders); a channel that would connect to another machine and has no testpath is not run. For a test
  environment; unlike ``runacceptancetest`` the clock and counters are not frozen. ``bots-portenv --local-folders``
  makes all folders of file channels inside the new environment, gives every other channel a testpath there and
  sets this.
- Database servers: interchanges are numbered and filled the same on every database. The order of the groups to
  envelope, of the routes of a run and the choice between matching translations are no longer left to the
  database: its collation may ignore case or punctuation, PostgreSQL sorts NULL last. Sorted as SQLite (and bots 3
  on it) does. Eight engine queries got ``ORDER BY idta``. Tested with the 42 official plugins on PostgreSQL 17,
  MySQL 8.4, MariaDB 11.4 and SQL Server 2022 as the database of bots.
- Error texts with ``debug`` on: the error line reads ``MessageError: ...`` as in bots 3, not
  ``bots.exceptions.MessageError: ...``.
- ``bots-portenv --bots3-dir-on-server=<dir>``: file channels with a relative path get the full path of the
  folder bots 3 used.
- New: ``bots-portenv --bots3=<directory of bots 3> [--number=N] <new environment directory>`` makes an
  environment from an environment of bots 3 in one go: usersys converted, a copy of the SQLite database
  upgraded, configuration carried over, usersys checked. Bots 3 is only read. ``MIGRATION.md`` is the guide
  for moving an installation.
- Packaging: install options ``[bots3]`` (what an installation from bots 3 usually needs), ``[sftp]``,
  ``[templatehtml]``, ``[mysql]``, ``[postgresql]``. Version ``4.0.0`` (first ``4.0.0rc4+stab1``); a build from a git repository
  without version tag no longer gets version ``0.0.postN``.
- New: ``bots-portconfig <config of bots 3> <config of the new environment> [--write]`` carries the
  configuration over: every option of the ``bots.ini`` of bots 3 that this bots knows (comments of the new
  file are kept; other name where it changed; reports what is not used any more), and from ``settings.py``
  the mail settings for error reports (to ``MAILERS``), managers, time zone, session settings and secret
  key. Without ``--write`` it only reports. The production installation changed 5 to 19 settings per
  environment.
- Web: a record of bots 3 can be saved again: a description longer than 256 characters (bots 3 did not check
  the length), and a database channel without host (the script makes the connection). "Change password" is in
  the menu by default again, as in bots 3 (``menu_changepassword``).
- ``bots.ini`` with a section or an option twice is read as python 2 did (the last value is used). 4.0
  stopped at start with ``DuplicateSectionError``; 7 of the 9 ``bots.ini`` files of the production installation
  that was checked have a section twice.
- Own logo and favicon per environment: ``[webserver]`` ``logo_image``, ``favicon_image`` (image files; shown in
  the page itself, the files of bots are not changed).
- About screen: own title and own support link via ``bots.ini`` (``[webserver]`` ``about_title``,
  ``support_url``, ``support_text``), instead of changing the template.
- Checked, already the same as 3.2.0: order of files in out-communication and of messages in an envelope
  (``ORDER BY idta``), user enveloping criterion when merging, log file viewer, menu "Retry failed
  out-communications", route names in the run menu are url-encoded, edifact viewer leaves indented files as
  they are.
- Json without the name of the root (``{...}`` instead of ``{"ROOT": {...}}``), for an installation that
  patched bots 3 to write it so: syntax ``named_root_object: False``. No change in the program; now with a
  test that one file per editype sets it for all grammars of an installation: the envelope grammar
  ``usersys/grammars/json/json.py`` (and ``usersys/grammars/jsonnocheck/json.py``) with only that syntax.

Work towards a release that existing bots 3.2.0 installations can move to. Ids (PAR-, API-, C-, WP- ...)
refer to the migration audit and its action plan.

Behaviour restored to bots 3.x:

- Incoming field values are stripped again by default: syntax ``strip_value`` is now True for csv, excel,
  edifact, x12 and tradacoms (C-03). Numeric fields ignore surrounding whitespace also when ``strip_value``
  is off; a trailing blank no longer adds decimals (PAR-13).
- ``botslib.addinfo()`` defaults ``statust`` to OK again in ``where`` and ``change`` (API-3).
- All exception classes and all ``botsconfig`` constants are reachable through ``botslib`` again
  (``botslib.BotsError``, ``botslib.CommunicationError``, ``botslib.FILEIN`` ...); ``GotoException`` is an
  alias of ``DummyException``; ``BotsError.msg`` works (C-04, C-17).
- x12: default syntax ``ISA14`` is ``'1'`` again; a value set by the mapping has priority, then syntax (C-22,
  API-5). A confirmrule ``ask-x12-997`` does not change ``ISA14`` any more (4.0 set it to ``'1'``): an
  installation with ``'ISA14': '0'`` in its x12 syntax and such a rule sends ``0``, as with 3.2.0. Found by
  running a bots 3.2.0 development environment through both versions.
- x12 997: confirmrules are evaluated per message (ST) again and only matching messages are acknowledged
  (PAR-12). The 997 grammar is ``997004010`` again, as bots 3. 4.0 used ``997<GS08>`` when usersys has that
  grammar, so a partner sending 004060 got its 997 in 004060 instead of 004010 (seen in the production
  replay: 22 of 22 997's). That choice is now a setting: ``[settings] x12_997_version_as_received = True``;
  with it an implementation suffix in GS08 falls back to ``997<first 6 of GS08>``, then ``997004010`` (PAR-5). Sender/receiver fall back to GS02/GS03 resp. UNB when the envelope grammar has no
  QUERIES (PAR-1).
- json: one message is written as an object, several messages as a list (as bots 3.x); syntax ``force_list``
  always writes a list (C-10). ``jsonnocheck`` output works again (WRT-1).
- ``trash`` channel registers the file as send (EXTERNOUT) again, so reports count it (C-38).
- Outgoing mail: channel field 'as body or as attachment' not set means attachment again (COM-4).
- Incoming mail: a header that mixes plain text and an encoded word is decoded, not rejected (COM-2); a mail
  without Subject or Message-ID is accepted (COM-3); text attachments keep their line ends (COM-23).
- ``sort()``: records without the sort key come first again (WRT-9).
- Configuration: a relative config directory (``-cconfig``, relative ``BOTS_CONFIG_DIR``) works again
  (API-17); ``log_file_number = daily``, lower-case log levels and a ``bots.ini`` without section
  ``[dirmonitor]`` are accepted (API-7, API-15).
- Enveloping: syntax parameter ``IDmode`` (``ISA_qualifier_GS``, ``ISA_qualifier``, ``UNB_qualifier``) and
  ``frompartner_outer`` / ``_inner`` / ``_qualifier`` in ``ta_info`` of envelope scripts (C-21). These are
  from ``master``; they are not in the 3.2.0 release.
- Enveloping: ``ta_info['reference']`` is a string again (C-20).
- Interchange counters: a counter with a name that is new in 4.0 (``isacounter_<sender>_<receiver>``,
  or sender taken from the syntax) continues where the bots 3 counter was, instead of starting at 1 (C-46).
- ``bots-updatedb`` is new (it was still the bots 2 to bots 3 script: no effect on PostgreSQL, errors on
  MySQL). It recognises an empty database, the database of bots 3 and of bots 4, and refuses anything else:

  - empty database: creates all tables, also ``ta``, ``mutex``, ``persist``, ``uniek`` (before: by hand
    from ``bots/sql``);
  - database of bots 3 (needs ``--yes-i-have-a-backup``): registers the existing tables, applies the
    changes, widens the columns of ``ta``, ``persist``, ``uniek`` that are wider in bots 4 (without this
    every file failed on PostgreSQL / MySQL: API-2), gives users the new ``view`` permissions for what
    they could see in bots 3 (C-50), lists the channels with a relative path (C-37);
  - ``--check`` reports and changes nothing; ``--createsuperuser`` for a new database.

  Checked with databases made by bots 3.2.0 on PostgreSQL 17, MariaDB 11.4, MySQL 8.4 and SQLite.
- The tables of bots-engine are part of the migrations (``0005``): ``migrate`` gives a complete database.
- No pending model changes on any supported Django (``makemigrations --check``): migration ``0004``,
  ``default_auto_field`` set (WEB-6). The help text of the channel field 'filename' was shown as a tuple.
- ``uniek.domein`` is 128 everywhere (was 35 in the model, 70 in the sql files, 35 after an upgrade): the
  counter names of 4.0 can be longer than 70 (WEB-9). ``persist.domein`` 70, ``persist.botskey`` 64.
- bots-engine on a database without its tables says so and tells to run ``bots-updatedb``, instead of
  '!Bots database is locked!' (DB-1).
- PostgreSQL: bots-engine works with psycopg2 as the only driver again (API-11); rows of a query can be read
  by position too (``row[0]``), as in bots 3 (DB-4); options in ``settings.py`` that are for django only
  (``isolation_level``, ``pool``, ...) are not passed to the driver.
- Counters (``unique()``): two processes can not draw the same number (checked with 4 processes on
  SQLite, PostgreSQL, MariaDB, MySQL).
- Cleanup deletes old reports in parts of 1000: with millions of reports one statement was too big for
  MySQL / MariaDB and nothing was deleted (COM-20).
- ``settings.py``: the MySQL example used ``storage_engine``, which MySQL 5.7+ does not know (DB-6).
- Editype ``excel`` works again (it could not work on python 3: PAR-2). ``.xlsx`` / ``.xlsm`` are read with
  ``openpyxl``, ``.xls`` with ``xlrd`` (``pip install bots-ediint[excel]``); the file is recognised by its
  content. Values are passed as in bots 3: whole numbers without decimals, dates as ISO date, errors as text.
- Preprocessing ``extractpdf`` works again, with ``pdfminer.six`` (``pip install bots-ediint[pdf]``); it used
  an interface that pdfminer no longer has, and wrote bytes into a text csv (COM-15).
- Route scripts: ``botsglobal.currentrun.get_minta4query_route()`` and ``get_minta4query_routepart()``
  are back (C-14).
- User exit ``accept_incoming_attachment`` with the arguments of bots 3 works: the arguments that are new
  in 4.0 (``content_disposition``, ``filename``) are only passed to a function that has them (C-19).
- ``import bots.usersys...`` in a user script imports from the usersys in use (part of C-45).
- ``pluglib.make_index(cleaned_data, filename)``: the order of arguments of bots 3 is accepted (C-33).
- ftp, ftps, ftpis receive in ASCII mode (the default of a channel): the bytes are written as received.
  4.0 decoded as UTF-8 and wrote latin-1: UTF-8 text was silently re-coded, other non-ASCII files were not
  received at all, and a CR on its own became LF (COM-1). This is what 3.2.0 does: bytes as received,
  line end CRLF as LF. (Only ``master`` refused files with non-ASCII bytes in ASCII mode.) After a failed transfer
  the answer of the server is read, so the next file is not affected.
- http(s) channels (new in 4.0):

  - parameters and headers are per channel and per file; a channel got the parameters and headers of the
    channels that ran before it in the same run (COM-5);
  - a channel with one parameter (``key=value``) sends it; a value can contain ``=`` and url-quoting
    (COM-6);
  - with debug 2 or higher every file ended in error after it was sent (COM-7);
  - 'mime encoding: ascii' on a file without content type gave an error (COM-8);
  - the second and later files of a run were posted to the url of the channel plus the name of the
    previous file: ``Uri.uri(filename=...)`` no longer changes the Uri object (COM-13);
  - a CA file (``ca_cert``, or ``caCert`` as in bots 3) is used for the channel itself, no longer set for
    the whole process via ``REQUESTS_CA_BUNDLE``;
  - ``pip install bots-ediint[http]`` installs ``requests``.
- TLS/SSL in channels (pop3s, imap4s, smtps, smtpstarttls, ftps, ftpis, https): two new fields in a channel,
  'Verify server certificate' (default on) and 'CA certificate file' (migration ``0006``).

  - 4.0 verified the certificate in every one of these channels except ftpis, without a way to switch it
    off: a channel of bots 3 to a server with a self-signed certificate stopped working (C-35). And ftpis
    accepted any certificate (COM-25).
  - Now all of them verify, unless switched off in the channel. ``bots-updatedb`` switches it off for the
    channels in a bots 3 database (bots 3 never verified) and lists the channels this concerns.
  - 'CA certificate file' can be used together with a client certificate ('Certificate chain file' with
    'Private key file'); before, a private CA and a client certificate could not be combined.
  - ftpis: ``parameters`` 16 and 17 could not work; the TLS version is negotiated, ``5`` demands TLS 1.2
    (COM-10).
- sftp: a private key of any type paramiko knows is read (RSA, ECDSA, Ed25519), with or without passphrase;
  it was RSA only, and with paramiko 4+ a user script asking for another type failed on the removed
  ``DSSKey`` (COM-11). Keys in ``parameters`` of the channel that paramiko does not know are ignored
  instead of breaking the connection (COM-26). The paramiko version is compared as a number.
- Two processes of bots starting at the same moment (engine, webserver, dirmonitor) could fail on creating
  the same directory.
- Web interface, security (all in functionality new in 4.0):

  - log viewer: on Windows a user with permission to view reports could read any file the webserver can
    read, eg ``config/settings.py`` with the ``SECRET_KEY`` (``?engine=../../../config/settings.py``):
    the name is now a file name only and has to be in the log directory (WEB-1);
  - source viewer: a ``.py`` file in a directory next to usersys with a name that starts the same
    (``usersys_old``) could be read (WEB-14);
  - a saved selection is read by name from the directory of the user only (WEB-15);
  - in these checks a backslash in a name is a separator on every platform, as on Windows: a name gives the
    same file (or the same refusal) on Linux and Windows;
  - file viewer: an incoming file with content type ``text/html`` ran its scripts in the session of the
    user who viewed it; it is now shown in a sandbox: no scripts, no access to the page of bots (WEB-8);
  - lists in the admin (channels, routes): an id or message type with html in it was shown as html; such
    values are escaped (WEB-21). The same for texts shown after reading a plugin.
- bots-dirmonitor:

  - never started a route on Windows: the name of a file in an event was compared in a way that could
    not match (SVC-1). On Linux a recursive watch did not see files in sub-directories (SVC-20), and a
    path written with ``//``, ``/../`` or relative never matched (SVC-21). Events are now matched on the
    name of the file and its directory, the same way on both platforms;
  - did not start with the ``bots.ini`` that is installed (sections ``[dirmonitorN]`` without ``path``:
    SVC-3);
  - ``--reload`` and the 'dirmonitor' tick of a route work on Windows; the threads that watch can be
    stopped (SVC-10);
  - watches first and looks for files that are already there after that; a file that arrived while
    starting or reloading was not seen;
  - sends the job as ``bots-engine``; the jobqueue-server knows where that is. Before, the job could be
    refused as 'Invalid task' (SVC-2);
  - a job that could not be sent because the jobqueue-server is away is sent when it is back;
  - new: ``[dirmonitor] trigger_on_modify = True`` (Linux) starts the route for every write to a file,
    as bots 3 did; default is once, when the file is closed (C-56);
  - usage text; 'Several routes to run for same watched path' was logged for every route (SVC-17).
- bots-jobqueueserver:

  - order of jobs: priority 1 first, within a priority first in first out. It was the reverse: lowest
    priority first, newest first (SVC-4);
  - accepts ``bots-engine`` by name (Windows: also ``bots-engine.exe``) and by the path it is installed
    in, also when PATH is not set for the daemon (SVC-2);
  - a job with output that is not UTF-8, a wrong priority, a job that can not start: logged, and the
    queue goes on (SVC-9, SVC-22); with ``killjobsintimeout`` the processes started by the job are killed
    too and the queue does not wait for them;
  - after 10 jobs in a row that can not start, new jobs are refused (code 6) instead of accepted and
    never run (SVC-11);
  - stop (SIGTERM, Ctrl-C): the running job can finish (``[jobqueue] stopwait``, default 60 seconds), the
    jobs that are not run are logged, exit code 0 (SVC-23); ``nr_threads`` is not used: jobs run one at
    a time;
  - listens on and is called via 127.0.0.1: on Windows each call via ``localhost`` took 2 seconds.
- Outgoing mail (smtp, mimefile):

  - mime-encoding 'never': the content of the file is in the mail as it is. 4.0 changed every line end in
    it (a LF or CR on its own) to CRLF (COM-9);
  - resend of a mail that was made by bots 3, or that was send in an automatic retry: the document is
    send again in a mail as before. It was send as the old mail inside a new mail (COM-24, C-41).
- bots-engine, start and exit:

  - the engine always ends. If at the end a thread is still running (started by a library or a user
    script) python waited for it for ever, with the database locked for the next run. Now the engine
    waits ``[settings] maxsecondsexit`` (default 30) seconds, logs which thread is running and where,
    removes the database lock and ends with its normal exit code (ENG-1);
  - a second engine for the same environment says on stderr why it does not run (exit code 3 as before);
  - ``log_when = report``: no error at exit when a log with the number of the run exists (Windows:
    COM-21);
  - the error report (mail) for a route that does not exist had the text with ``%(route)s`` as subject
    and a dict as text (COM-12);
  - zip of outgoing files: only the files made in the route-part itself, as in bots 3 (COM-18).
- ``bots-configure`` works on python 3.13 and later (SVC-5); ``bots-plugoutindex`` works (SVC-6).
- json (functionality new in 4.0, unless said otherwise):

  - boolean fields (format ``B``) could not be written (WRT-3) and not be read: a value was checked as
    a number. A boolean is ``True`` / ``False`` in a mapping; ``true``, ``false``, ``1``, ``0`` are accepted;
  - 'a record with MAX 1 as object instead of a list' never worked (WRT-4). It works now, but only when
    asked for with syntax parameter ``'max1_as_object': True``. Default is as bots 3 writes json: records
    in a record are always a list. (The default of 4.0 would have changed every json bots 3 writes, had
    it worked.) ``force_list`` is for the list of messages only;
  - a list of values in a file: the values are strings, as every value in bots; objects in the same list
    are records; a list for a field that can not be repeated is error [J57] instead of an internal
    error (PAR-6);
  - empty content (``{}``, ``[]``) is ``[J52]: No usable content`` again, not an internal error (PAR-7,
    regression);
  - jsonnocheck: ``{"order": {...}}`` is read as a message with root ``order`` again, as in bots 3. 4.0
    put it in a record ``ROOT``, so ``inn.get({'BOTSID': 'order', ...})`` found nothing (C-09,
    regression). If ``defaultBOTSIDroot`` is set in the grammar that is the root, as in 4.0.
- Web interface, screens and actions:

  - 'Resend All' in the outgoing screen did nothing: the button had the name of 'Rereceive All' (WEB-3);
  - setting 'refresh' in a screen logged the user out after the interval: the page posted its first
    form, which is the log-out form (WEB-22). The same mistake in deleting a saved selection;
  - 'Run engine' from the menu waited until the engine was ready, as long as the run took (WEB-4), and
    needed ``bots-engine`` in the PATH of the webserver (WEB-5): the engine is started with the python
    of the webserver and the request returns at once. ``/bots/runengine?clparameter=--new`` without a
    character after ``runengine`` showed the home page and ran nothing (WEB-18);
  - menu 'Manual confirm' showed the wrong files (WEB-7); a text filter with two spaces gave error 500
    (WEB-10); ``/bots/filer?idta=abc`` gave error 500 (WEB-11, regression);
  - 'Log out' on the password pages gave error 405 on django 5 and later (WEB-13);
  - values of one request (title of the window, shortcuts of the user) could show up in a request
    handled at the same time (WEB-16);
  - code lists in the admin as a user that is not superuser: error 500 on PostgreSQL (DB-3);
  - the 404 page of the webserver had a broken title (WEB-17).
- New: ``bots-portusersys <source> <destination>`` converts the user scripts of bots 3 to python 3: a
  usersys directory, a plugin or a zip with grammars. It makes imports of a file next to it explicit
  (``from recordsD96AUN import recorddefs`` -> ``from .recordsD96AUN import ...``), converts python 2
  syntax and names (with python library ``fissix``: ``pip install bots-ediint[port]``), writes a file
  that is not utf-8 as utf-8, compiles every file, and lists the lines that are valid python 3 but can
  work differently (cmp, encode/decode, loops over a set, ...). The source is not changed.
- New: ``bots-checkusersys`` checks the usersys of an environment as bots-engine uses it: compiles every
  python file, reads every grammar with the checks of a translation, imports every script.
- Extra ``tools`` asked for ``pdfminer`` (the python 2 library); now ``pdfminer.six``.
- Mapping scripts: ``transform.partnerlookup``: a partner of which the field is empty is 'not found'
  again (exception, or with ``safe`` the value or None); 4.0 returned ``''`` (C-15). The 3rd parameter
  can be given by its bots 3 name ``field_where_value_is_searched`` (C-16).
- Mapping scripts: the constants of ``botsconfig`` via ``transform`` (``transform.TRANSLATED``,
  ``transform.ID``: C-17); ``inn.envelope`` is ``inn.envelope_content`` (C-18; a name from ``master``, not in
  the 3.2.0 release).
- Syntax parameters ``no_results_if_any_error_in_translation_edifile`` (now ``KillWholeFile``) and
  ``allow_spaces_between_records: False`` (now ``strict_syntax_check: True``) work by their older
  names; they were ignored without notice (C-25). These names are from ``master``, not from the 3.2.0 release.
- Configuration: a ``settings.py`` of bots 3 is refused at start with the reason and what to do; it was
  read without error and then nothing in the web interface worked (C-44). ``bots.ini``:
  ``use_email_address_validation`` works by its bots 3 name (C-47); a relative ``usersys`` is looked for
  in the environment first, not in the bots package.
- Error of a file (in the database, in the web interface, in the error mail) is the error itself again.
  4.0 put the python errors that led to it in front: ``'NoneType' object is not subscriptable ... The
  above exception was the direct cause of the following exception ...`` (PAR-3).
- An error that is handled (reported for the file) is no longer written to the log as ERROR with a
  traceback; the traceback is logged at level DEBUG (API-12). 'Parse & passthrough' of a file is not an
  error in the log (API-13).
- A numeric field with ``_`` in it is not a number: python 3 reads ``1_0`` as 10 (PAR-10).
- ``bots-grammarcheck``: a grammar that can not be imported gives the error, not a traceback (SVC-19).

Fixes of defects that are also in bots 3 (checked with ``master``):

- edifact interchanges with functional groups (UNB-UNG-UNH) are split into messages (PAR-4).
- fixed files with ``noBOTSID``: record length is calculated correctly (PAR-11).
- ``getdecimal()`` returns 0 for a non-numeric value, as documented (WRT-11).
- Texts of errors: [A67] had an empty position (PAR-9); grammar error 'field length has to be greater
  than nr of decimals' had an empty length (WRT-12).

Fixes in functionality new in 4.0:

- ``putraw()`` works (WRT-2); ``sort(..., sort_decimal=True)`` works (WRT-5); ``inn.sort()`` /
  ``out.sort()`` accept the keyword arguments (WRT-6).
- csv ``skip_firstline`` on an empty file (PAR-8).
- Texts: [A69] had an empty position (PAR-9); the allowed formats of a field were shown as
  ``dict_keys([...])`` (WRT-15); the debug line for a partner syntax was never written (WRT-10).
- Merging: messages for which the mapping set different envelope data are no longer merged into one
  interchange under the envelope data of the first group (API-1); merging only collects messages of the
  route itself; an error in one group no longer marks the result of another group as failed.
- x12: ``GS04`` set in the mapping is used for versions before 004010 too (API-4).
- ``BotsConfig.get()``: an explicit default, also ``''``, is never an error; ``[dirmonitorN]`` without
  ``route`` is "no route".
- ``bots/config/bots.ini`` (used with ``-cconfig`` in a source tree) is the same as the install template;
  it no longer switches on acceptance-test mode (API-8).

Plugins:

- A python plugin index (``botsindex.py`` of bots 2/3) is parsed, not executed; python 2 long literals
  (``10L``) are accepted (C-30). No use of ``zipimport.load_module`` (removed in python 3.15).
- Reading a plugin is all-or-nothing again: a failing plugin leaves nothing in the database (SVC-7).
- Files in a plugin can not be written outside usersys/botssys (SVC-8).
- All files under ``usersys/`` in a plugin are installed, not only ``.py``/``.html`` (C-31).
- Plugin versions are compared as numbers (SVC-14).

Other fixes:

- ``import bots`` works from a source tree without installed distribution metadata (SVC-15).
- Initialisation with an absolute config/usersys path no longer fails under import hooks on Windows (SVC-18).
- ``txtexc()`` no longer fails when called before logging is initialised (API-12).

Tests:

- ``tests/regression``: 42 official plugins are run and compared with stored results of bots 3.2.0
  (python 2.7): run counters and every output file.
- ``tests/unit``: unit tests on a temporary bots environment.
- The bots 3 unit test scripts moved to ``tests/legacy`` (not ported yet).


4.0.0rc4 (2026-09-05)
------------------
- Python 3 only >= 3.10
- Django 5 & 6 support
- Bugs fixes
- Added responsive ui support
- views.filer: Fix xml indent == '0' display in some cases
- More universal and readable log format: "asctime levelname [logname] message"
- botstable: Updates & enhancements
- confirmrule enhancements: admin, 'confirmasked' ruletype added for x12
- envelope.x12: Dynamic ISA14 depending on confirmrule ask-x12-997
- inmessage.tradacoms: Fix: Add missing function set_syntax_used()
- Add strip_value grammar syntax parameter for inmessage (EDIFACT, X12, TRADACOMS, CSV)


3.8.5 (2023-05-30)
------------------
- admin/base.html: Fix nav-bots with django < 4
- bots.css:
    - Fix/clean --header-* color vars
    - Add styles to datetime clock
    - Updates/Fixes sticky positions


3.8.4 (2023-05-22)
------------------
- [UI] Add theme switch support (django >= 4.2)
- [UI] Add sticky bars (nav-bots, breadcrumbs, ...)
- document.html: Add log link
- admin/routes: Clear alt value when no translateind


3.8.3 (2023-04-08)
------------------
- botsinit: console log format is now same as file log format
- configure: Fixes locals() vars


3.8.2 (2023-03-30)
------------------
- locale/fr: Update
- views.(document, process): Update titles
- nav/documents.html: Remove useless PROCESS link
- Cleaning usage text of console-scripts
- Outgoing: Fix statust filter display for exclude values
- Fix js view_translate() for incoming, outgoing and document views
- document.html: Add filter/exclude to status field
- botstable:
    - No display of filter for already filtered field
    - No display of exclude if exclude value is not in field.options


3.8.1 (2023-03-24)
------------------
- nav/allruns.html: Add nav/documents.html: All Phases
- bots.ini[webserver] Add menu_changepassword
- filer: Add indent (json, xml, html)
- reports.html: Add dropdown filters to row.status and row.type
- bots.ini[webserver]: Add log_cherrypy_access (default: False)
- admin.py: Remove classes: wide, extrapretty, add get_form


3.8.0 (2023-03-03)
------------------
- locale/fr: Updates

- confirm: Fix displayed buttons when filtered

- models.routes: Same notindefaultrun value to all sequences of a route

- Fixes for Py2:
    - __init__.py for initbotsenv
    - models.py:    glob recursice arg need Py >= 3.5
    - transform.py: queries formating cleaning
    - admin.py:     Fix ModelAdmin.log_change
              :     Fix bugged js part
    - forms.py:     Fix not valid py3 syntax (v, *list)
    - templates:    Fixes for old django<2 translate > trans
    - botslib:      last fixes for ascii row keys needed by query()

- Drop support Django < 1.11

- Change name of all saved plugin to: bots_plugin_xxxxxx.zip

- views.py:
    - Remove cleaning of cleaned_data for idta and/or reportidta keys
    - Better args request parsing

- forms.LIMITS: Add 150 and 200 (items per page)
- [UI] Add save and delete selection to all views with botstable
- [UI] Better display performances
- botslib.Uri(): Little fix
- botslib.botsinfo_display(): added
- bots.config.settings.USE_TZ = False
- pluglib.py: Update, fixes & cleaning
    - plugout_backup_core() and delete() moved from views.py
- models.py: Add list_usersys(), get_userscripts() moved from admin.py

- envelope.py: Fix default envelope_content for envelope()

- [UI] Date/time:
    - displayed with settings.DATE(TIME)_FORMAT
    - DATE/TIME_INPUT_FORMAT context

- [UI] Add icons (py, filter, log, user, group, logfiler(*)
- filer: Add numbered lines
- inmessage.x12.handleconfirm: Fix checkconfirmrules
- List grammars and mappings in subdirectories
- templates/403_csrf.html: New


3.7.15 (2022-12-03)
------------------
- [UI] Fix unclickable link in translate change_list page opened from a route change_form
- [UI] bots(-nav).css:
    - Fix nav-bar border
    - Add box-shadow
- [UI] *filer.css:
    - Add background-color filer and source content
    - Add css/dark_mode.css
    - Add & update colors
- [UI] Scale new window open by popup()

3.7.14 (2022-12-01)
------------------
- locale/fr: Update
- webserver.py: Add custom CherryPy error 404 page for static path
- bots/install/settings.py: Add [session,CSRF]_COOKIE_NAME

3.7.13 (2022-07-04)
------------------
- bots/nav/config.html: Add channel/[in,out]/Add [in,out] channel
- bots/channel/change_form.html: Fix remove field display for add channel
- refresh.html: Stop refresh page when selector is set with no value
   - This avoid refreshing page when selector change to no value
- bots-configure: Init and display user Bots config environment
- botsinit: initbotsenv() added, called in generalinit()
   - Now clean bots env is created at first run

3.7.12 (2022-05-28)
------------------
- bots.css: Add botsstatus4 text color for dark scheme
- models.channel.routes_link(): Added, in admin channel list_display
- channel/change_form.html: Hide remove field for out channel
- admin/bots/change_form.html: Add obj_title block in content_title block
  This fix title in add translate and channel admin view.
- admin routes: Add link to translates

3.7.11 (2022-05-19)
------------------
- __init__.py: default_app_config is no more used in Django >= 4
- link/confirmation.html: Add refresh button for pending confirmation
- views.logfiler: Fix max engine log files displayed (25) with log_when=report
- logfiler.html: Add link to top in subtitle
- communication.sftp: Fix paramiko.logger.level from channel.debug
- dirmonitor.process_existing_files(): Skip route.fromchannel not removed files
- dirmonitor/jobqueueserver: Verify if jobqueue is running with 'isup' task
- templates/bots/nav/[custom,shortcuts] Fixes for Django 4

3.7.10 (2022-05-12)
------------------
- dirmonitor.py: Linux Fixes/updates thread notifier and reload

3.7.9 (2022-05-02)
------------------
- views.runengine: Add redirect to reports
- views.runengine: Clean/update log and message
- bots.ini: Add log_when: daily, report (default - replace log_file_number = idta)
- bots.ini: log_file_number could be specified for [webserver, jobqueue, dirmonitor]
- views.document: Fix allstatus catch when idta is specified

3.7.8 (2022-03-23)
------------------
- Update locale/fr
- botstable/td/confirmed.html: Update for manual confirm
- bots/link/confirmation.html: Fix pending displayed for not confirmasked docs
- models.routes.dirmonitor: Update help_text

3.7.7 (2022-03-22)
------------------
- bots/select*.html: Add clear all filters button
- Update confirmations: confirmed, unconfirmed, pending ...
- admin: change_form title: channel: Add type, translate: Add fromeditype
- bots/js/vars.html-> bots/js/urls.html
- forms.DocumentForm: Add allstatus and filename
- models.py: Update for dirmonitor, add reload_dirmonitor(), ...
- dirmonitor.py: Update usage()

3.7.6 (2022-03-12)
------------------
- admin.py: Routes/Channel: title with filter values in change_list
- bots.css: botslink: Use default color: var(--link-fg)
- User shortcuts: Fix perms & exclude other user shortcuts
- communication.py: Updates & fixes reference[:128] > [:256]
- admin.py: Clean fix actions, more docsting

3.7.5 (2022-03-10)
------------------
- dirmonitor.linux_event_handler: Better events catch
- dirmonitor.add_job(): Log and catch send return error and sendbotserror
- Update services exit log
- botsinit.generalinit(): Add djediint.bots init
- dirmonitor: Update admin activation with others dirmonitored routes

3.7.4 (2022-03-07)
------------------
- config/settings.py: Default botssys is now in ~/.bots/env/$USER/botssys
- dirmonitor: Add trigger to reload conf while running
- incoming.html: Add filter by reportidta in dropdown menu
- admin.ChannelAdmin.list_filter: Add 'debug'
- communication.LoggerPipe: Better log display (imap4(s), smtp(s))

3.7.3 (2022-02-22)
------------------
- Add shortcuts menu for custom and user shortcuts urls
- Selected lines are now colorized
- filer.html: Fix sticky title & html/pdf height
- forms.py: LIMITS: add 250
- botsinit.py: LOG_LEVELS: STARTINFO=28, START=27, DONE=26, COM=25, STDOUT=11, STDERR=12
- models.(report,filereport): Add delete():
   - Add delete reports from ui. (cascade filereport(s) and ta related entries)
   - Add forms.incoming.reportidta
- communication.py: http debug log content and response depend on level
- admin.py: Add debug in channel list_display
- communication.py: Add stderr2log(): All debug log > engine.log
   - Now communication debug log are logged into engine.log
- models.ta.reference: max_length 128 > 256
- bots/filer.html: Better display for html/pdf content (full height)

3.7.2 (2022-02-11)
------------------
- botsinit.py: LOG_LEVELS: Add START: 25, DONE: 26, STARTINFO: 25 > 27
- envelope.envelope(): Fix json.loads() with empty ta_info['rsrv5']

3.7.1 (2022-02-10)
------------------
- jobqueueserver: Updates, add security enhancement, log (stderr, stdout)
   - Restrict tasks that could be run (bots-engine), Add others in bots.ini
   - stderr and stdout of job could now be logged.
   - If job exit with error, this is now logged.
- job2queue: Update & Fix start bug introduce with I18N JOBQUEUEMESSAGE2TXT
- admin.routes: Better display of dirmonitor in list_display
- logfiler.html: Add refresh button for current log (process.log)

3.7.0 (2022-02-08)
------------------
- forms.ReportsForm: Add type filter (new, resend, rereceive, retry)
- [templates] Display (from/to)channel (type) (file, ftp, http, smtp, ...)
- Increase len of models:
   - ta.reference, ta.divtext, ta.rsrv1 to 128
   - report.rsrv1 to 256
- Incoming email attachment filename > ta.divtext
- Add download file link after all filer link
- [templates] Add botstable/dropdown/*.html, update botstable/td/*, bots/link/*
- Update loglevel to INFO start/end route and channel communication
- communication.py: Set debug level from channeldict['debug']
- Fix infinite loop with communication.http.incommunicate()
- dirmonitor: Now watch routes fromchannel (file) with active dirmonitor
- bots-filer.css: Fix for several ta in idtas filer.html
- views.logfiler: Better download filename
- views.runengine(): Fix message and log level
- models.py: increase, clean, add routes.dirmonitor, channel.debug:
   - Add models.routes.dirmonitor: implementated in bots-dirmonitor
   - Add models.channel.debug: implemented in communication.py
- [core] Updates from eppeye-bots/bots3.3:
   - Json filed type
   - enveloppe access from mapping
   - ...
- communication.py: add filename parameter to accept_incoming_attachment
- outmessage.xml(): Remove python26 part
- PY3 module import first
- pluglib.py: plugout_files() Fix default charsetdirs os path (win)
- admin.py: Record activate/deactivate actions in Django object history
- communication.py: sftp: use keyfile; remove pycrypto depency, check for paramiko version; more comments
- update validate email
- router.py: Fix resend if mime


3.6.2 (2021-12-29)
------------------
- Add forms.View.actions and multiline select (incoming, outgoing, confirm):
   - Select several lines (incoming, outgoing, confirm) to run action:
     delete, rereceive, resend, manual confirm.

3.6.1 (2021-12-27)
------------------
- bots-icons.css: Change ico-run
- forms.py: Increase some CharField max_length to 512 (filename, ref, ...)
- js/refresh.html: Fix infinite reload loop when invalid form is posted
- templates/bots/botstable: Cleaning paths: Move td_*, thead_* > td/* thead/*
- botstable/checkbox_field.html: checkbox button style (lastrun, admlink, popup)
- clear_*.html: Update delete icons, now displayed with css class
- forms.py, outgoing.html: Add testindicator filter field

3.6.0 (2021-12-24)
------------------
- locale/fr: Update
- Add bots/refresh.html bots/js/refresh.html to bots/base.html
- botsinit.py: Little change of logging format
- Add admin/index.html admin/login.html
- Big update on web part: icons, filters line, cleaning views, ...
- Updates, fixes and clean: forms.py, views.py, viewlib.py
- favicon.ico -> bots.ico
- Add admin/js/bots.js and (from/to)messagetype selector in routes admin
- Refactor and clean javascript part of selectors of translate admin and now in routes admin.
- css: Update color values by var(--xxxx) from django
- admin.py: TranslateAdmin: Permit {editype}/{editype}.py messagetype
- get_grammars() could list edifact/edifact.py, x12/x12.py, ...
- Add bots/templates/bots/link/grammarsrc.html
- Cleaning for botslink css class in templates/bots/link/*
- bots.js: Fix add_class_sortedby() in some cases
- admin/base.html: Add block favicon in block extrastyle
- forms.py: Fix ConfirmForm.confirmed initial=''
- models.py: Update script_link* (script_link2 > script_viewlink)
- Add bots/link/messagetype.html
- Add (from/to)messagetype and tscript selectors for translate admin
- admin.py: Clean translate with read only perms
- admin.py: Fix & clean for translate list_display and perms script view
- Add bots/translate/change_form.html with view src link
- admin.py: Add perms to script links (route, comscript, grammars, mapping)
- Change script icon: icon-yes.svg > icon-viewlink.svg


3.5.4 (2021-09-17)
------------------
- bots.css: Fix user-tools links color
- Add favicon in srcfiler.html
- Add favicon in logfiler.html
- Fix arg sep link (; > &) in nav/(in-out)xoming.html,
  Django doen't support ';' arg request separator anymore.

3.5.3 (2021-09-10)
------------------
- Update usertools and userlinks blocks in templates/
- Fix password_change

3.5.2 (2021-09-05)
------------------
- change_form: Update for Django > 3.2 with new subtitle block

3.5.1 (2021-09-05)
------------------
- change_form: Better title with app name, model.verbose_name and entry name
- change_list: Better title with app_name and model._meta.verbose_name_plural

3.5.0 (2021-09-03)
------------------
- views.py: Updates & fixes GET request?* & ?select&*
- botslib.txtexc(limit=0): Parametize limit of traceback.format_exc(limit=limit)
- botslib.txtexc(): Log all calls: botsglobal.logger.error(terug)
- Add errors links in in/out/allrun nav
- Add GET request with fields value & permanent link on all views
- Add (from/to)partner_tochannel routes admin filters


3.4.9 (2021-06-21)
------------------
- Add admin filters for routes, translate, partner:
   - Partner admin view can be filtered by partnergroup
   - Add from/to partner filters in routes and translate admin view
   - add from/to messagetype, tscript, alt filters to translate admin view

3.4.8 (2021-05-23)
------------------
- Add make bots plugin admin actions:
   - route without translate
   - grammar plugin
   - translate plugin without grammar (entries and mappings scripts only)

3.4.7 (2021-05-17)
------------------
- Fixes & update models.scripts_link*, add scriptname in srcfiler.html title
- Better error display
- exceptions log level raise to ERROR in transform.py
- log level for exception up to ERROR for botslib.log_session
- Fix security in views.srfiler()
- Fix botslib.botsinfo() with sqlite db settings without user, host

3.4.6 (2021-01-14)
------------------
- Update/fixes permissions: admin, views, bots/nav/*.html
- New: make plugin from admin selection: ccodes, channel, routes,...
- make_plugin with queryset include all related entries and files:
   - routes: add related channels + scripts, partners + scripts
   - translate with mappings and grammars except for edifact/x12 without route.alt set
- Fix pluglib.read_index2database:
      django.db.models.fields.FieldDoesNotExist > django.core.exceptions.FieldDoesNotExist
- Fixes plugins*/plugout* views: form.action for delete
- Filters selections with several values and negative filtering rule
- Lots of fixes and update on ui
- Update boslib.Uri() and comunication.http path and filename
- Add missing fields (rsrv2, rsrv4) to filterlist in botslib._Transaction
- Add popup to all views: add _popup field in BotsForm
- Fix & Update logger.level

3.4.5 (2020-11-26)
------------------
- Add bots.apps for django apps config
- Fix/update bots.views.server_error()
- Update for django.setup() in botsinit.generalinit()
- Update bots-menu with bots-nav templates

3.4.4 (2020-11-10)
------------------
- Update bots environment infos display by engine log
- Fixes for Py2, super() call in class need class xxx(object)

3.4.3 (2020-09-21)
------------------
- Fix services launch by systemd in settings.py
- Fix bug with engine log file introduce logging name change in 3.4.2
- Change/Fix botsinit.BotsConfig().get()
- Update config/settings.py install/settings.py

3.4.2 (2020-09-09)
------------------
- Cleaning logging: logger.name = __name__
   - 'bots.webserver'
   - 'bots.jobqueueserver'
   - 'bots.dirmonitor'
   - ...
- Console log with timestamp
- Fix LOGIN_REDIRECT_URL = /bots/home in settings.py

3.4.1 (2020-09-03)
------------------
- Prefix bots views urls path: /bots/(in..,out..,report,...) 
- Now auth_patterns could be imported from bots.urls
- [UI] Fix bots menu integration with others nav bar (Django 3, ...)
- Update for Django 4 ugettext() > gettext()
- Django 3 compatibility, remove python_2_unicode_compatible in models.py
- Clean/add fields in all bots.ini
   log_file_number = idta
   compatibility_mailbag = False
   nr_threads = 1
   unow = utf_8
- Delete counter in admin are now allowed execept internals
- [ui] remove save_on_top for Ccodetrigger and Uniek in admin.py
- [ui] Fix title in link/logfiler.html
- [ui] Better menu, config>* submenus (routes, chan, ...)
- Add fromchannel, tochannel to routes list_filter in admin.py
- Add clear_filter for date fields when value
- node.display*() now use logger.info() instead of print()
- Add verification for imported settings in generalinit()
- Fix xml2botsgrammar with python3
- Fix & clean whatched recursive directories in dirmonitor.py
- Fix for Node, cast part results to string if enhancedget with list

3.4.0 (2020-03-02)
------------------

- Update all views with nicer botstable headers using filtered field menu.

- Added saving selection in select to recall a selection in view and select.

- Add botsmenu context to have possibility to customize menu like botslogo.


3.3.4 (2019-12-18)
------------------

- filer.html improvement, display html and pdf files.

- Download file in filer, now check editype/contenttype to set appropriate filename extention.

- templatehtml could access to ta_info, like ta_info['reference']
  in template.html and envelope.html to.

- Parametize and add templatehtml engines: genshi, django (for now)
  maybe more in future like jinja2, but genshi is already powerfull

- Add save_on_top for all admin change_form

- Update for new engine log file stored by idta,
  now param in bots.ini [settings] log_file_number is 'idta'.
  That store engine.log in logging/engine/idta of each run.

- Better title display for logfiler

- Update logging formating


3.3.3 (2019-10-14)
------------------

- Better display in views with colorized status

- New logging system available for engine, log could be keeped and viewed for each report

- Log files now have it's own process directory (logging/engine/.., logging/webserver/..)

- Some fixes


3.3.2 (2019-10-02)
------------------

- jobqueue fully fixed and now work as expected.

- dirmonitor now check files at starting.

- xml indent could be parametized with string like 'indented': '\t',

- Remove ``persistfilters.py``. already in Django > 1.6.

- Add local/fr for French translations.

- Big cleaning and littles fixes on all pythons files



3.3.1 (2019-07-18)
------------------

- Full Python 3 support

- Updated ``setup.py`` and build methods

- Update for tests

- Latest CherryPy support

- Django 2 support

- New datetime picker from https://github.com/xdan/datetimepicker

- Restore jobqueueserver. It was broken in 3.3.0 because of unfinished
  python2/3-support. Fixes https://github.com/bots-edi/bots/issues/21.
  [WouterVH]

- Remove ``bots_importlib``. Python2.6 is no longer supported.
  Cfr. https://github.com/bots-edi/bots/issues/23
  [WouterVH]

- Remove ``bots_ordereddict``. Python2.6 is no longer supported.
  Cfr. https://github.com/bots-edi/bots/issues/22
  [WouterVH]

- Add rst-version of GPL3-license.
  Thanks to https://github.com/shibukawa/rest-licenses/
  [WouterVH]

- Updated ``MANIFEST.in``.

- Add ``setup.cfg`` with config-settings for several tools.
  Also set ``bdist_wheel`` to ``universal``.
  [WouterVH]

- Move unittests to ``tests``-subdirectory.
  [WouterVH]

- Move scripts to ``scripts``-subdirectory.
  [WouterVH]


3.3.0 (2016-11-23)
------------------

- Add ``License.rst``
  [WouterVH - 22-11-2016]

- Update Readme, and .gitignore
  [JCapriotti - 19-11-2016]

- add setup.py using setuptools
  [WouterVH - 09-08-2016]

- add .gitignore-file
  [WouterVH - 09-08-2016]

- Revert ``Added gitignore and sphinx docs``
  [eppye - 08-03-2016]

- Revert ``Added gitignore and sphinx docs``
  [eppye - 08-03-2016]

- Merge pull request #367 from abhishek-ram/sphinx-docs
  Added gitignore and sphinx docs
  [eppye - 07-03-2016]

- Added gitignore and sphinx docs
  [ Abhishek Ram - 31-10-2015]

- last chagnes?
  [eppye - 15-08-2015]

- small change in text for 'ftp account'
  [eppye - 04-08-2015]

- Issue 362: add: more preprocessing
  [eppye - 21-05-2015]

- type in internal function name: save_int instead of safe_int
  [eppye - 21-05-2015]

- Issue 253: migrate to python 3.*
  python3 uses another pickle protocol by default.
  [eppye - 20-05-2015]

- change in comments
  [eppye - 20-05-2015]

- added some unittests.
  [eppye - 20-05-2015]

- small change i order to get unittests right: transform.getcodeset gets a list from ccodes.
  postgreSQL returns this in 'reversed' order.
  not an error, but use same orders as MySQL and SQLite
  [eppye - 20-05-2015]

- Issue 254: for persist: timestamp on update
  [eppye - 20-05-2015]

- Issue 359:  Add option for daily engine.log
  [eppye - 20-05-2015]

- Issue 341: Optionally add ``run cleanup`` to run menu. Allow cleanup run from commandline in acceptance testing.
  (missed some code at first try)
  [eppye - 20-05-2015]

- Issue 338: Error when incoming email with subject > 35 chars and db is not SQLite
  [eppye - 20-05-2015]

- Issue 347: bots_communication_failure counters: domein too long for db field
  [eppye - 20-05-2015]

- Issue 358: cleanup.py should not log ``vacuum database`` for non-sqlite installations
  [eppye - 20-05-2015]

- Issue 363: add: function to split up text (or lists)
  [eppye - 20-05-2015]

- change in comments
  [eppye - 20-05-2015]

- Issue 360: mapping is the centre of bots,
  set email-addresses from mapping
  [eppye - 19-05-2015]

- Issue 355: add: easier access to all envelope fields in mapping
  changed this again: envelope fields are in inn.envelope: a list of dicts: [mpath,mpath,etc]
  [eppye - 19-05-2015]

- Issue 360: mapping is the centre of bots
  - outcommented mysterious assignged to topartners in transform.py/_translate_one_file ; it does not do anything.
  - changes in comments
  [eppye - 16-05-2015]

- change in comments
  [eppye - 16-05-2015]

- Issue 328: pass frommail and tomail to mapping
  during testing found: tomail was not passed if there was no check on the toaddress.
  changed this, tomail is now always passed.
  [eppye - 15-05-2015]

- Issue 356: set all envelope fields from mapping
  - more data is passed for merging - so more data will get passed from maping script
  - more comments
  - fixed soem inconsistenties in enveloping
  [eppye - 13-05-2015]

- small code change for use in acceptance tests: get a frozen value for datetime objects.
  (needed this in some mappig scripts).
  [eppye - 12-05-2015]

- change in comments
  [eppye - 12-05-2015]

- Issue 355: add: easier access to all envelope fields in mapping envelope fields are in:
  inn.envelope (a dict), not in ta_info anymore.
  [eppye - 11-05-2015]

- small code change for use in acceptance tests: get a frozen value for datetime objects.
  (needed this in some mappig scripts).
  [eppye - 25-04-2015]

- Issue 355: add: easier access to all envelope fields in mapping
  [eppye - 23-04-2015]

- Improve & bug fix for Issue 353: add: function to 'strip diacritics'
  - one function (instead of 2)
  - can handled other charsets (not only ascii and latin1/iso-8859-1)
  - one char -> one char or nothing - but not eg 2 chars; better because fields lenghts should not get 'suddenly' bigger in edi
  [eppye - 22-04-2015]

- Issue 357: Add: pass to mapping number of messages and sequence number in file/interchange
  [eppye - 22-04-2015]

- Issue 354: better handling of partners in x12 (edifact)
  pick up combination of ISA-ID/ISA-qual/GS-ID.
  improved coding of enhancedget.
  [eppye - 17-04-2015]

- Issue 353: add: function to 'strip diacritics'
  [eppye - 16-04-2015]

- Issue 349: In translations, grammars not required for db or raw types, so do not show error icon
  [eppye - 15-04-2015]

- Issue 253: migrate to python 3.*
  roll back: callable() is available in python >= 3.2
  [eppye - 11-04-2015]

- small code/errors improvement:
  - different warning for missing frompartner and topartner
  - checking in subroutine: same for x12, edifact etc.
  [eppye - 11-04-2015]

- Issue 352: new: very strict checking on whitespace 'between' records
  [eppye - 11-04-2015]

- Issue 351: add: sanity checks on separators (edifact/x12)
  [eppye - 10-04-2015]

- Issue 348: set/change headers via user scripting
  [eppye - 09-04-2015]

- max integer was not tested correctly.
  limit here is the database: int is 2^31 -1
  to change that, have to change database -> next database migration
  [eppye - 09-04-2015]

- Issue 337: Add bots_environment_text in page title
  [eppye - 07-04-2015]

- Issue 340: Admin views minor changes for better usability
  [eppye - 07-04-2015]

- Issue 341: Optionally add ``run cleanup`` to run menu. Allow cleanup run from commandline in acceptance testing.
  [eppye - 06-04-2015]

- Issue 346: added option: when arything goes wrong in translation, skip whole file /no output
  [eppye - 03-04-2015]

- change in comments
  [eppye - 03-04-2015]

- Issue 345: remove in communication.py option to userscript keyfile, certfile
  [eppye - 03-04-2015]

- Issue 342: Add logfile viewer in GUI
  [eppye - 03-04-2015]

- change in comments.
  [eppye - 03-04-2015]

- restructured code for fixed files with noBOTSID
  [eppye - 02-04-2015]

- Issue 344: bug when re-using structures (in grammar)
  Other things for grammars/grammarreading:
  - more consistent fucntion calls (no more defaults)
  - much more comments in grammar.py
  - code is better structured.
  - soem extra checks were not performed bacause of typo
  [eppye - 02-04-2015]

- Issue 253: migrate to python 3.*
  in unittests: same conversion 'trics' as in source code
  [eppye - 02-04-2015]

- Issue 253: migrate to python 3.*
  [eppye - 01-04-2015]

- get grammar/grammar reading clearer:
  - changes in comments
  - no more defaults in grammar read functions - that only obscures things.
  [eppye - 31-03-2015]

- small change in coding: read/write pickled files via botslib.
  [eppye - 30-03-2015]

- change in comments.
  [eppye - 30-03-2015]

- Issue 334: better errors for numeric fields with exponentials
  [eppye - 30-03-2015]

- Issue 333: bug: charsets of incoming emails
  [eppye - 30-03-2015]

- minor change/improvement in logic of file->email mime.
  [eppye - 30-03-2015]

- Issue 332:  in node.change: convert eg int to string (like in put())
  [eppye - 30-03-2015]

- Issue 331: changed 'out_as_inn' implementation (same functionality)
  also other changes; see change for  Issue 253:  migrate to python 3.*
  [eppye - 30-03-2015]

- Issue 330: removed 'persistfilter' in GUI
  [eppye - 30-03-2015]

- Issue 329: filtering incoming email: add 'multipart/related' to whitelist_multipart
  [eppye - 30-03-2015]

- Issue 328: pass frommail and tomail to mapping
  [eppye - 30-03-2015]

- Issue 327: add more parameters to user exits for 997/CONTRL
  [eppye - 30-03-2015]

- Issue 326: edifact/UNA segment: if repetition seperator is space, assume they make a mistake
  plus: typo: seperator -> separator
  [eppye - 29-03-2015]

- Issue 325: fix bug in grammar read logic
  [eppye - 28-03-2015]

- Issue 324: other way of indicating unique part in filename
  [eppye - 28-03-2015]

- Issue 318:  mimefile msgid may exceed 70 chars (too big for database)
  [eppye - 28-03-2015]

- Issue 323: rollback Issue 314
  [eppye - 26-03-2015]

- Issue 253: migrate to python 3.*
  [eppye - 26-03-2015]

- Issue 319: better xml-generating
  [eppye - 26-03-2015]

- Issue 320: better json generating - sorted!
  [eppye - 26-03-2015]

- Issue 321: improve outgoing formatting fields
  [eppye - 26-03-2015]

- bug in bots 3.2.0. not serious/no harm.
  [eppye - 10-09-2014]

- bug in 2.3.0. Not very serious.
  [eppye - 10-09-2014]

- 2 bugs in bots 3.2.0 (reported by ludovic)
  [eppye - 10-09-2014]

- changes in comments
  [eppye - 10-09-2014]

- update windows build batchfiles.
  [eppye - 04-09-2014]

- correct version
  [eppye - 03-09-2014]

- ready for release 3.2.0
  [eppye - 01-09-2014]


3.2.0 (2014-09-02)
------------------

- TODO


3.2.0rc2 (2014-05-27)
---------------------

- TODO


3.2.0rc (2013-05-27)
--------------------

- TODO

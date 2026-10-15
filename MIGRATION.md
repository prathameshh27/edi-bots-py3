# Moving a Bots 3 installation to this Bots

For the administrator of a Bots 3.x installation (Python 2) who moves it to this version (Python 3).
It describes the steps, what the tools do, what has to be done by hand, and what behaves differently.

Everything here works on copies. The Bots 3 installation is only read, and can keep running until the switch.

## In short

```
pip install "bots_ediint-<version>-py3-none-any.whl[bots3]"

bots-portenv --bots3=<directory of bots 3> <new environment directory>
```

Then: look at what `bots-portenv` reports, fix the listed lines in your mappings, set the folders of the file
channels, test, and switch over.

## 1. Install

- Python 3.10 or newer.
- Install in a virtual environment of its own; do not mix with the Python 2 of Bots 3.

```
python -m venv <somewhere>/bots4
<somewhere>/bots4/bin/pip install "bots_ediint-<version>-py3-none-any.whl[bots3]"
```

`[bots3]` adds what an installation that comes from Bots 3 usually needs: the conversion of Python 2 scripts
(`fissix`), SFTP (`paramiko`), HTML templates (`Genshi`), http channels, excel and pdf input. Other options:

| Option | For |
|---|---|
| `[mysql]` | Bots' own database in MySQL/MariaDB, or communication scripts that `import MySQLdb` |
| `[postgresql]` | Bots' own database in PostgreSQL |
| `[sftp]`, `[templatehtml]`, `[http]`, `[excel]`, `[pdf]`, `[port]` | The parts of `[bots3]` one by one |

The commands have the names of Bots 3 without `.py`: `bots-engine`, `bots-webserver`, `bots-jobqueueserver`,
`bots-dirmonitor`, `bots-job2queue`, `bots-grammarcheck`.

## 2. Make the new environment

One environment of Bots 3 (config, usersys, botssys) becomes one environment directory of this Bots.

```
bots-portenv --bots3=/opt/bots/bots  /srv/bots/env/production
```

For an installation with several environments next to each other (`config2`, `usersys2`, `botssys2`):

```
bots-portenv --bots3=/opt/bots/bots --number=2  /srv/bots/env/env2
```

Or name the three places yourself: `--usersys=`, `--config=`, `--database=` (the SQLite file).

What it does:

| Step | What | Result |
|---|---|---|
| 1 | Makes the directory with `config`, `botssys`, `usersys` | It must not exist yet, or be empty |
| 2 | Copies usersys, converted to Python 3 | Lines to look at: `port-review.txt` |
| 3 | Copies the SQLite database and upgrades the copy | Routes, channels, partners, translations, users, counters and history are there |
| 4 | Carries `bots.ini` and `settings.py` over | Listed on screen |
| 5 | Reads every grammar and imports every script of the new usersys | Errors on screen and in `port-check.json` |

Exit code 0: nothing to look at. 1: done, with things to look at. 2: not done.

**A test environment on another machine** (eg testing on Windows what runs on Linux): add `--local-folders`.

```
bots-portenv --bots3=D:/copy/of/bots --number=2 --local-folders D:/bots-test/env2
```

- Every folder of a file channel is made inside the new environment, `<env>/channels/<path as it was>`, also the
  Linux paths (`/home/edi/in` becomes `<env>/channels/home/edi/in`). Put test files there.
- Every other channel (FTP, SFTP, mail, database) gets a test folder `<env>/channels/test/<in or out>/<channel>`,
  and `bots.ini` gets `channels_use_testpath = True`: these channels read from and write to their test folder.
  A channel without a test folder is not run at all. Nothing is sent to, or fetched from, a partner.
- Unlike the acceptance-test mode of Bots 3, the clock and the counters are not frozen.
- When the environment is going to be used for real, remove `channels_use_testpath` from `bots.ini` and set the
  real folders.

Stop Bots 3 (or make sure no run is going) while the database is copied, or work from a backup of it.

Every command of this Bots takes the environment with `-c<environment>/config`, or from the environment
variable `BOTS_CONFIG_DIR`.

The steps can also be done one by one: `bots-portusersys`, `bots-updatedb`, `bots-portconfig`,
`bots-checkusersys`. Each explains itself when started with `--help`.

## 3. Your mappings and scripts

The conversion to Python 3 is mechanical: `print`, `except X, e`, imports of a file in the same folder,
`has_key`, `xrange`, `unicode` and the like. It does not change what a script means. Some things mean something
else in Python 3 without being an error; these lines are listed in `port-review.txt`:

| Listed as | What changes | What to do |
|---|---|---|
| division | `7/2` is `3` in Python 2 and `3.5` in Python 3 | Use `//` where a whole number is needed (slice, index, `range`, counter). Without it: `TypeError: slice indices must be integers` |
| loop over a dict | Python 2 gave the keys in an arbitrary but fixed order; Python 3 in the order they were added | If the loop writes records, the order of the output changes. Use a list, or `sorted()` |
| set | The order of a loop over a set can differ per run | `sorted(set(...))` |
| pickle / persist | Values stored by Python 2 | Read by this Bots; check if you store your own classes |
| encode / decode, binary file | Text is `str`, data is `bytes` | Check the line |
| `cmp`, `keys()[0]`, `map(...)[0]` | Not in Python 3, or not a list | Rewrite |

Both `//` and a list are valid in Python 2 too, so these fixes can be made in the Bots 3 installation first.

Files that cannot be imported are reported in step 5. Usual causes: a backup copy with dots or blanks in its
name (leave it out), a helper module that was next to the Bots program instead of in usersys (copy it into
usersys), a library that is not installed in the new Python.

`import bots.usersys...`, `from bots.botsconfig import *`, `bots.botslib`, `bots.transform` and the exits and
their arguments work as in Bots 3.

## 4. Configuration

`bots.ini`: every option of the old file gets its value in the new one. Three options have no function any
more and are reported: `lauchfrequency` of the job queue and of the directory monitor (jobs start at once), and
`compatibility_handle_message_errors`. A `bots.ini` with a section twice is read as Python 2 read it.

`settings.py` is another file than in Bots 3; the old one cannot be used as it is. Carried over into the new
one: `MANAGERS`, the mail server for error reports (as `MAILERS`), `SERVER_EMAIL`, `TIME_ZONE`, session
settings, `SECRET_KEY`.

Not carried over: the database. All environments with the default SQLite work at once. If Bots 3 used MySQL
or PostgreSQL: start `bots-portenv` with `--no-database`, set `DATABASES` in the new `settings.py`, point it at
a copy of the Bots 3 database, and run `bots-updatedb --yes-i-have-a-backup`.

Branding: `[webserver]` `about_title`, `support_url`, `support_text`, `botslogo`, `environment_text`.

## 5. Channels

- **Folders of file channels.** A relative path of a file channel was relative to the directory of the Bots 3
  program. It is now relative to the new environment directory. `bots-updatedb` lists these channels. Either
  give them a full path, or make the folders in the new environment.
- **Certificates.** Bots 3 did not check the certificate of a server. Channels that come from a Bots 3 database
  keep connecting as they did ("Verify server certificate" is off). New channels check it. Switch it on per
  channel when you know the server has a valid certificate.
- **Database channels.** The scripts work unchanged after conversion. Install the driver they import
  (`[mysql]` for `MySQLdb`). New, and optional: set the field "Database" of the channel (MySQL/MariaDB,
  PostgreSQL, SQLite or SQL Server) and Bots makes the connection; see chapter 11. The order in which a script returns its messages follows Python 3 rules if it
  comes from a dict (see "loop over a dict"): the same messages, possibly in another order.
- **SFTP.** Private key scripts (`privatekey`) and scripts that replace a method of the channel class work as
  they are. The host key of the server is checked only if a `hostkey` script supplies it, as in Bots 3.
- **FTP in ASCII mode** changes line ends, as it did.
- **Mail.** `subject`, `accept_incoming_attachment` and the other exits are called as in Bots 3.

## 6. Data and history

- **Counters** (interchange control numbers, message numbers, file name counters) are in the database and
  continue where Bots 3 stopped.
- **History** (incoming, outgoing, reports) is in the database and is shown.
- **The files themselves** are in `botssys/data` of Bots 3 and are not copied by `bots-portenv`. Copy that folder
  to `botssys/data` of the new environment if you want to look at old files, re-send or re-receive them. The
  layout is the same.
- **Files in transit.** A file that Bots 3 received but did not finish (in error, or waiting) can be processed
  by this Bots, also an object of a database channel stored by Python 2.
- **Clean-up** removes the same as Bots 3 with the same settings.
- **Users and passwords** stay. Users that could change something can also see it (this version has a
  separate right to view).

## 7. What is different from Bots 3

Output of translations was compared file by file on a production installation of nine environments (8,400
received files) and is the same, with these remarks:

| Subject | Difference |
|---|---|
| JSON | Same content. Python 2 wrote a blank at the end of lines after a comma and the keys in arbitrary order; now no blank and the keys in the order of the grammar |
| Order of output from scripts | Where a script loops over a dict or a set, see chapter 3 |
| Error texts | The error itself, without the Python traceback in front of it. The traceback is in the log at level DEBUG |
| x12 997 | Made in version 004010, as Bots 3. `x12_997_version_as_received` in `bots.ini` gives the version of the received message |
| Job queue, directory monitor | Start a job at once; file changes are seen sooner |
| `bots-engine` | Always ends, also when a thread of a library hangs (`[settings] maxsecondsexit`) |
| Web interface | Other look. Menu items the same; "Change password" in the Home menu |
| Local changes in the Bots 3 program | Are not in this Bots unless listed in the change log. Known and covered: JSON without the name of the root (`named_root_object`), XML via editype `mailbag` |

`CHANGELOG.rst` has every change with its reason.

## 8. Test before the switch

1. `bots-checkusersys -c<config>` gives no errors that matter.
2. Web interface: `bots-webserver -c<config>`, log in, look at routes, channels and the history.
3. A run that cannot reach a partner. Do **not** rely on acceptance-test mode alone: it only replaces a channel
   that has a "test path". Give every channel of the copy a test path, or change the channels of the copy to
   local folders, before the first `bots-engine`.
4. Put files that were received earlier in the incoming folders and compare the result with what Bots 3 made.
5. If possible, a period in which the new environment gets a copy of the live input and writes to folders.

## 9. The switch, per environment

1. Stop the scheduler entry, job queue and directory monitor of Bots 3. Wait for a running engine to end.
2. Back up the Bots 3 database and usersys.
3. Run `bots-portenv` again into a fresh directory (the database is then current), and redo what was done by
   hand: the fixes in mappings (or have them in Bots 3 already), the folders of file channels.
4. Copy `botssys/data` if wanted.
5. Start the new job queue, directory monitor and web server; point the scheduler at the new `bots-engine`.
6. First run: check the control number of the first interchange per partner, and the report.

## 10. Going back

Nothing in the Bots 3 installation was changed. To go back: stop the new one, start the old scheduler entries.
Files that the new Bots received and sent in between are not in the history of Bots 3, and its counters did
not move: set the counters (table `uniek`) to the values of the new environment before the first run, or a
partner gets a control number twice.

## 11. Databases

### The database of Bots itself

| Database | Install option | `ENGINE` in `settings.py` | Note |
|---|---|---|---|
| SQLite | (none) | `django.db.backends.sqlite3` | The default; one file per environment |
| PostgreSQL | `[postgresql]` | `django.db.backends.postgresql` | |
| MySQL / MariaDB | `[mysql]` | `django.db.backends.mysql` | Django 6.1 needs MySQL 8.0.11+ or MariaDB 10.11+ |
| Microsoft SQL Server | `[mssql]` | `mssql` | New. SQL Server 2016 or newer; see below |

A new, empty database is filled with `bots-updatedb`. A database of Bots 3 (SQLite, PostgreSQL, MySQL) is
upgraded in place by the same command; make a copy first. Bots 3 had no SQL Server, so there is nothing to
upgrade there: start with an empty database and move the configuration with a plugin (Bots menu "Plugins").

SQL Server in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'bots',
        'HOST': 'sqlserver.example.com',
        'PORT': '1433',
        'USER': 'bots',
        'PASSWORD': '...',
        'OPTIONS': {
            # without an ODBC driver (python library mssql-python, part of [mssql]):
            'python_driver': 'mssql_python',
            # or with the ODBC driver of Microsoft: 'driver': 'ODBC Driver 18 for SQL Server',
            # a server with its own (not trusted) certificate:
            'extra_params': 'TrustServerCertificate=yes',
        },
    }
}
```

### Channels of type `db`

Bots 3 left the connection to the communication script (`connect`, `disconnect`). That still works. New: set
the field "Database" of the channel, and Bots makes the connection:

| Field | Meaning |
|---|---|
| Database | MySQL / MariaDB, PostgreSQL, SQLite or Microsoft SQL Server |
| Host, Port | The server (port empty: the usual port of that database) |
| Username, Password | The account |
| Path | The database name; for SQLite the file. Empty: "Filename" is used, as the Bots 3 scripts did |
| Parameters | Driver options as `name=value;name=value`, eg `sslmode=require` (PostgreSQL), `TrustServerCertificate=yes` (SQL Server) |

The communication script then only has the function that does the work:

```python
def incommunicate(channeldict, dbconnection):
    cursor = dbconnection.cursor()
    cursor.execute("SELECT * FROM orders WHERE status = %(status)s", {'status': 'Ready'})
    rows = cursor.fetchall()
    cursor.execute("UPDATE orders SET status = 'Send' WHERE status = 'Ready'")
    return [rows]                      # one message with all rows; or a list with one item per message

def outcommunicate(channeldict, dbconnection, db_object):
    cursor = dbconnection.cursor()
    for line in db_object:
        cursor.execute("INSERT INTO received (po, qty) VALUES (%(po)s, %(qty)s)", line)
```

- The connection is the same for all four databases: parameters as `%(name)s` with a dict or `%s` with a list,
  rows as dicts (`row['po']`) that can also be used by position (`row[0]`). One script works on each database,
  as far as its SQL does.
- Bots commits when the function ends without error, and rolls back when it raises an error; the file is then
  in error and can be retried. The script does not commit.
- The driver comes with the install option of that database (see the table above).
- A script that has `connect` keeps making its own connection, also when the field is set.

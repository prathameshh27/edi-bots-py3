# Tests

```
pip install pytest pytest-xdist            # next to the bots dependencies
pytest                                     # tests/unit and tests/regression
pytest tests/unit                          # seconds
pytest tests/regression -n 4               # about two minutes with 4 workers
pytest tests/regression -k x12             # a selection of plugins
```

No test reads or writes your own bots environment (`~/.bots`): each creates a temporary environment.

The environments and files the tests make go into `<project>/.temp/tests` when the directory that contains
`bots-new-stable` has a directory `.temp` (or into `$BOTS_TEST_TEMP` if that is set), otherwise into the temp
directory of the system. They are removed after a test that passes. Small files of single tests use pytest's
own `tmp_path`.

## tests/unit

Unit tests. `conftest.py` creates one bots environment per test session in a temporary directory and
initialises bots on it; `helpers.py` writes grammars into that environment, parses files and writes
messages in-process.

## tests/regression

Every official plugin under `plugins/` is loaded into a fresh environment, the engine is run once in
acceptance-test mode (frozen clock) and the result is compared with `golden/`.

- `plugins/<set>/<name>.zip`: the official plugins (`base` = bots 3 plugins, `bots2`, `user` = user
  contributed). Their database index and test files are untouched. Their python files were ported to
  python 3 mechanically: implicit relative imports rewritten (`from recordsD96AUN import recorddefs` ->
  `from .recordsD96AUN import recorddefs`) and `2to3`. Nothing else was changed.
- `golden/<set>/<name>/golden.json` and `outfile/`: what **Bots 3.2.0 on python 2.7** (Django 1.7.11,
  SQLite) did with the original plugin: run counters, status per input file, and every output file.
  Bots 3.2.0 is the release: github `eppye-bots/bots`, branch `bots32` (the `master` branch of that
  repository is later, unreleased development and behaves differently for 13 of these 42 plugins).
- `test_plugins.py` documents, at the top, the few accepted deviations from that reference with their
  reason: json files are compared by content (3.2.0 writes the fields of an object in arbitrary order),
  outputs of Bots 2 era plugins that contain the date of the run, and four files of mappings that loop over a
  python `set`.

When a plugin fails its work directory is kept (path in the assertion message; `engine.log` in it).

The reference data was produced by running each original plugin with that release under python 2.7
(Django 1.7); it does not have to be regenerated to run the tests.

Also in this directory, each test in its own environment (fixture `botsrun` in `conftest.py`):

- `test_mail.py`: mail in and out through `mimefile` channels (no mail server needed).
- `test_database.py`: `bots-updatedb` on SQLite: the database of bots 3.2.0 (`data/botsdb_3.2.0_sqlite`, as
  installed by that release), an empty database, the database shipped with bots 4, a database that is not bots.

## tests/database

`dbmatrix.py`: the same checks of `bots-updatedb` on PostgreSQL 17, MariaDB 11.4 and MySQL 8.4, each started
in a docker container that is removed afterwards. Not collected by pytest (needs docker and the drivers
`psycopg` and `mysqlclient`): `python tests/database/dbmatrix.py <workdir>`. `dumps/` are databases made by
bots 3.2.0 itself on these servers.

## tests/legacy

The unit test scripts of bots 3 (`unit*.py`). Not ported: they need test plugins that are not in the
repository and initialise bots on the developer configuration inside the package. Not collected by pytest.

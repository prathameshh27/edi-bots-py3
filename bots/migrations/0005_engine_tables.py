"""
Tables of bots-engine that django does not manage (ta, mutex, persist, uniek):
- create them if they do not exist (new database);
- widen the columns that are wider in bots 4 than in bots 3 (database made by bots 3).
"""
from django.db import migrations

from bots import dbschema


def engine_tables(apps, schema_editor):
    # pylint: disable=unused-argument
    dbschema.ensure_engine_tables(schema_editor.connection)


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0004_model_details'),
    ]

    operations = [
        # nothing is undone when migrating backwards: the tables contain the data of the edi-transactions
        migrations.RunPython(engine_tables, migrations.RunPython.noop),
    ]

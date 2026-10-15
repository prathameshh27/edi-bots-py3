# Channels of type 'db': bots makes the connection for the kind of database set here.

import bots.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0006_channel_verify_cert_cafile'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='dbengine',
            field=bots.models.StripCharField(blank=True, choices=[('', '(script makes the connection)'), ('mysql', 'MySQL / MariaDB'), ('postgresql', 'PostgreSQL'), ('sqlite', 'SQLite'), ('mssql', 'Microsoft SQL Server')], default='', help_text='For type "db": the kind of database. Bots makes the connection with host, port, username and password; the database is "path" (for SQLite: the file), or else "filename". Driver options in "parameters", eg sslmode=require (PostgreSQL) or TrustServerCertificate=yes (SQL Server).<br>The communication script then only needs incommunicate or outcommunicate. Empty: the script makes the connection itself (connect and disconnect), as in bots 3.', max_length=35, verbose_name='Database'),
        ),
    ]

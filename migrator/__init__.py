from emotes.wsgi import db, app
import functools
from playhouse.migrate import *
from emotes.app.models import *
from datetime import datetime
from peewee import *

migrator = MySQLMigrator(db.database)
migrations_dict = {}

def migration(timestamp):
    def migration_decorator(f):
        migrations_dict[datetime.strptime(timestamp, "%Y%m%d_%H%M%S")] = f
        return f
    return migration_decorator


from emotes.migrator.cli import *
from emotes.migrator.migrations import *

migrations_dict = sorted(migrations_dict.items(), key=lambda x: x[0])

def migrate():
    try:
        version = Version.select().get()
    except ProgrammingError:
        from emotes.install import install
        install()

        version = Version(version=migrations_dict[-1][0])
        version.save()

        return # We installed, so nothing more to do.


    index_begin = 0

    for index, i in enumerate(migrations_dict):
        if version.version < i[0]:
            print("Migrations were found. Migrating DB...")
            index_begin = index


    migrations_to_apply = migrations_dict[index_begin:]

    for date, migration in migrations_to_apply:
        migration()

    version.version = migrations_dict[-1][0]
    version.save()

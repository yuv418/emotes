from emotes.wsgi import db, app
import functools
from playhouse.migrate import *
from emotes.app.models import *
from datetime import datetime, time
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
    if migrations_dict == []:
        print("No migration tasks to do.")
        return

    try:
        version = Version.select().get()
    except ProgrammingError:
        from emotes.install import install
        install()

        version = Version(version=datetime(1970, 1, 1))
        version.save()


    index_begin = -1

    for index, i in enumerate(migrations_dict):
        if version.version < i[0]:
            print(f"Migrations were found. Executing migration from {i[0].strftime('%Y-%m-%d %H:%M:%S')}...")
            index_begin = index

            i[1]()
            version.version = i[0]
            version.save()

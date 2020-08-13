from emotes.wsgi import db, app
import functools

migrator = MySQLMigrator(db)
migrations_dict = {}

def migration(timestamp):
    def migration_decorator(f):
        migrations_dict[timestamp] = f
        return f
    return migration_decorator


from emotes.migrator.cli import *
from emotes.migrator.migrations import *


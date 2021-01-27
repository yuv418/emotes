from emotes.migrator import migrator, migration
from peewee import *
from playhouse.migrate import *
import traceback

@migration("20210127_153515")
def migration_20210127_153515():
    """Put your migration here."""

    migrate(
        migrator.add_column("resizedimage", "webp", BooleanField(default=False))
    )

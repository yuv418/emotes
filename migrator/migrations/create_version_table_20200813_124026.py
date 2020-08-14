from emotes.migrator import migrator, migration
from playhouse.migrate import *

@migration("20200813_124026")
def migration_20200813_124026():
    """Put your migration here."""

    migrate(
        migrator.add_column('version', '')
    )

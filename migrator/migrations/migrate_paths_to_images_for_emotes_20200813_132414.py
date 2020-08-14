from emotes.migrator import migrator, migration
from playhouse.migrate import *
from emotes.app.models import *

@migration("20200813_132414")
def migration_20200813_132414():
    """Put your migration here."""
    print("hi")

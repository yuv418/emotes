from emotes.migrator import migrator, migration
from emotes.app.models import *
from playhouse.migrate import *

@migration("20210129_135137")
def migration_20210129_135137():
    """Put your migration here."""
    print("Here")

    admin = User.get(User.admin == 1)

    global_nmsp = Namespace(name="Global", slug="", user_id=admin.id)
    global_nmsp.save()

    # Link emotes to namespace

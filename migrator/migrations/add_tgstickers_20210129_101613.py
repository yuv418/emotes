from emotes.wsgi import app
from emotes.migrator import migrator, migration
from emotes.app.models import *
from peewee import *
from playhouse.migrate import *
from uuid import uuid4

@migration("20210129_101613")
def migration_20210129_101613():
    """Put your migration here."""
    migrate(
        migrator.add_column("namespace", "tg_stickerpack_name", TextField(default=""))
    )

    for nmsp in Namespace.select():
        nmsp.tg_stickerpack_name = Namespace.random_stickerpack_name()
        nmsp.save()


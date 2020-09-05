from emotes.migrator import migrator, migration
from playhouse.migrate import *
from emotes.app.models import *

@migration("20200813_203428")
def migration_20200813_203428():
    """Put your migration here."""

    emotes = Emote.select()

    for emote in emotes:
        try:
            if emote.path:
                print(f"Migrating emote {emote.name} to image.")

                new_image = Image(original=emote.path, emote=emote)
                new_image.save()

                new_image.size(32, 32)
                new_image.size(48, 48)
                new_image.size(64, 64)
                new_image.size(128, 128)
                new_image.size(256, 256)

                migrate(
                    migrator.drop_column('emote', 'path')
                )
        except AttributeError:
            migrate(
                migrator.add_column("emote", "path")
            )
            migration_20200813_203428()





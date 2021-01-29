from emotes.migrator import migrator, migration
from emotes.app.models import *
from playhouse.migrate import *
import copy

@migration("20210129_143940")
def migration_20210129_143940():
    """Put your migration here."""
    migrate(
        migrator.add_column("resizedimage", "tg_file_id", TextField(default="")) # Sticker file id
    )

    old_resized_images = ResizedImage.select().where((ResizedImage.width == 256) & (ResizedImage.height == 256) & (ResizedImage.webp == True))
    print(old_resized_images)

    for rszimg in old_resized_images:
        if rszimg:
            print(f"{rszimg} is id")
            img = copy.copy(rszimg.image)
            rszimg.delete_instance()

    # size all emotes
    images = Image.select()
    for image in images:
        if image.original.split(".")[-1] != "gif": # not animated
            image.size(256, 256, webp=1)

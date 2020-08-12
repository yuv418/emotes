from emotes.wsgi import db, app
from emotes.app.models.emote import *
from peewee import *
from playhouse.signals import Model, pre_delete
from titlecase import titlecase
from werkzeug.datastructures import FileStorage
import os
import json
import string
import secrets

alphanumeric = string.ascii_letters + string.digits
class Image(Model):
    """Model to keep track of resized images as part of emotes."""
    original = TextField() # Path to original image
    emote = ForeignKeyField(Emote, backref='images', unique=True)

    class Meta:
        database = db.database

    @staticmethod
    def from_file(emote: Emote, file: FileStorage):
        """
        Creates this image and runs tasks to cache 32x32, 48x48, 64x64, 128x128, and 256x256 version resized images.
        """
        file_ext = file.filename.rsplit(".", 1)[1]
        if file_ext in app.config["ALLOWED_EXT"]:
            filename = ''.join([secrets.choice(alphanumeric) for i in range(64)]) + f".{file_ext}"
            file.save(os.path.join(app.config["UPLOADS_PATH"], filename))

            print(f"Creating with emote {emote}")
            new_image = Image(original=filename, emote=emote)
            new_image.save()

            return new_image

    def size(width, height):
        """Returns a processed ResizedImage of the size requested. If the image doesn't exist, this will create it, and return an unprocessed ResizedImage."""
        pass


@pre_delete(sender=Image)
def delete_image(model_class, instance):
    emote_path = os.path.join(app.config["UPLOADS_PATH"], instance.original)
    try:
        os.remove(emote_path)
    except FileNotFoundError:
        # Doesn't matter. Could just be missing a file, so we can fail silently?
        pass

    for resized_image in instance.resized_images:
        resized_image.delete_instance()


class ResizedImage(Model):
    path = TextField(default=None)
    width = IntegerField()
    height = IntegerField()
    processed = BooleanField(default=False)

    image = ForeignKeyField(Image, backref='resized_images')

    class Meta:
        database = db.database

@pre_delete(sender=ResizedImage)
def delete_resized_image(model_class, instance):
    resized_emote_path = os.path.join(app.config["UPLOADS_PATH"], instance.path)
    try:
        os.remove(resized_emote_path)

    except FileNotFoundError:
        # see reasoning in other pre_delete
        pass

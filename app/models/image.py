from emotes.wsgi import db, app
from emotes.app.models.emote import *
from peewee import *
from playhouse.signals import Model, pre_delete
from titlecase import titlecase
from werkzeug.datastructures import FileStorage
from emotes.app.tasks.resize import resize_image
from time import sleep
import os
import json
import string
import secrets

alphanumeric = string.ascii_letters + string.digits
class Image(Model):
    """Model to keep track of resized images as part of emotes."""
    original = TextField() # Path to original image
    emote = ForeignKeyField(Emote, backref='images', unique=True, null=True)

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
            file.stream.seek(0)
            file.save(os.path.join(app.config["UPLOADS_PATH"], filename))

            print(f"Creating image with emote `{emote.name}`")
            new_image = Image(original=filename, emote=emote)
            new_image.save()

            new_image.size(32, 32)
            new_image.size(48, 48)
            new_image.size(64, 64)
            new_image.size(128, 128)
            new_image.size(256, 256)

            return new_image


    def size(self, width, height, webp=False):
        """Returns a processed ResizedImage of the size requested. If the image doesn't exist, this will create it, and return an unprocessed ResizedImage.
        If webp=True, then it will generate a webp for this size."""

        print(f"Size method for image for {width}x{height} with webp {webp}")

        resized_image = ResizedImage.select().where((ResizedImage.width == width) & (ResizedImage.height == height) & (ResizedImage.webp == webp) & (ResizedImage.image == self)).first()
        type = 'emote'

        if not self.emote_id: # This is a local emote
            dirname = os.path.dirname(self.original)
            info_path = os.path.join(dirname, "info.json")

            with open(info_path) as info_f:
                info = json.load(info_f)
            if info['type'] == 'gif':
                type = 'aemote'
            else:
                type = 'emote'
           
        if resized_image:
            print(resized_image.height)
            if not resized_image.processed:
                if not self.emote_id:
                    if type == 'emote':
                        resize_image(resized_image.id, webp)
                        return resized_image

                resize_image.apply_async(args=[resized_image.id, webp], countdown=0) # sad face
                return resized_image

            return resized_image

        resized_image = ResizedImage(width=width, height=height, image=self, webp=webp)
        resized_image.save()

        if not self.emote_id:
            if type == 'emote': # If this is an emote, we can resize it if it hasn't been resized synchronously since there won't be a significant performance impact.

                task = resize_image(resized_image.id, webp)
                resized_image = ResizedImage.get(ResizedImage.id == resized_image.id) # Reload model so changes and updates are reflected.

                return resized_image

        task = resize_image.apply_async(args=[resized_image.id, webp], countdown=0) # sad face

        return resized_image

@post_save(sender=Image)
def autosize(model, new_image, created):
    """Auto-size commonly used sizes of emotes."""

    print("Running sizings")
    new_image.size(32, 32)
    new_image.size(48, 48)
    new_image.size(64, 64)
    new_image.size(128, 128)
    new_image.size(256, 256)
    new_image.size(256, 256, webp=True)



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
    webp = BooleanField(default=False) # These are TELEGRAM webps -- meaning all of them are 512x512 wrapped.

    image = ForeignKeyField(Image, backref='resized_images')
    tg_file_id = TextField(default="")

    class Meta:
        database = db.database

@pre_delete(sender=ResizedImage)
def delete_resized_image(model_class, instance):
    if instance.processed: # Only do if it was resized.
        resized_emote_path = os.path.join(app.config["UPLOADS_PATH"], instance.path)

        try:
            os.remove(resized_emote_path)

        except FileNotFoundError:
            # see reasoning in other pre_delete
            pass

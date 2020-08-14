from emotes.wsgi import db, app
from emotes.app.models.namespace import *
from emotes.app.models.image import *
from peewee import *
from playhouse.mysql_ext import JSONField
from playhouse.signals import Model, pre_delete, post_save
from playhouse.hybrid import *
from titlecase import titlecase
import os
import json

class Emote(Model):
    name = CharField()
    slug = CharField()
    info = JSONField()
    namespace = ForeignKeyField(Namespace, backref='emotes')

    @hybrid_property
    def image(self):
        try:
            return self.images.get()
        except Exception: # Doesn't exist.
            return None

    @staticmethod
    def local_emotes() -> list:
        """Get a list of dictionaried local emotes."""
        emotes_details = []
        emotes_dirs = os.listdir(app.config["EMOTES_PATH"])
        emotes_names = [titlecase(emote_dir.replace("-", " ")) for emote_dir in emotes_dirs]
        for emotes_dir in emotes_dirs:
            emotes_dict = {}
            emotes_info_path = os.path.join(app.config["EMOTES_PATH"], emotes_dir, "info.json")
            with open(emotes_info_path) as emotes_info_f:
                emotes_info_dict = json.load(emotes_info_f)

                if emotes_info_dict.get('name'): # Currently, local emotes don't have a name field, so we have to autogenerate one. TODO require all local emotes to have a name.
                    emotes_dict['name'] = emotes_info_dict['name']
                    del emotes_info_dict['name']
                else:
                    emotes_dict['name'] = titlecase(emotes_dir.replace("-", " "))

                emotes_dict['slug'] = emotes_info_dict['path'].split(".")[0]
                del emotes_info_dict['path']

                emotes_dict['info'] = emotes_info_dict


            emotes_details.append(emotes_dict)


        return emotes_details


    @staticmethod
    def local_emote(slug=None, name=None) -> dict:
        """Get a local emote based on a provided slug or name. If the function can't find a local emote based on your criteria, it returns None"""
        local_emotes = Emote.local_emotes()
        for local_emote in local_emotes:
            if local_emote['slug'] == slug or local_emote['name'] == name:
                return local_emote

        return None

    class Meta:
        database = db.database

@post_save(sender=Emote)
def create_linked_image(model_class, instance, created):
    from emotes.app.models.image import Image # This is very much a hack.
    print(instance)
    new_image = Image.from_file(instance, instance.file)
    new_image.save()


@pre_delete(sender=Emote)
def delete_uploaded_emote(model_class, instance):

    # TODO make these celery tasks, since deleting can take a while.
    if instance.image:
        instance.image.delete_instance()


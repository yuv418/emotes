from emotes.wsgi import db, app
from emotes.app.models.namespace import *
from peewee import *
from playhouse.mysql_ext import JSONField
from playhouse.signals import Model, pre_delete
import os

class Emote(Model):
    path = TextField()
    name = CharField()
    slug = CharField()
    info = JSONField()
    namespace = ForeignKeyField(Namespace, backref='emotes')

    class Meta:
        database = db.database


@pre_delete(sender=Emote)
def delete_uploaded_emote(model_class, instance):
    emote_path = os.path.join(app.config["UPLOADS_PATH"], instance.path)
    os.remove(emote_path)

    print(f"Deleted emote {emote_path} from uploads successfully.")
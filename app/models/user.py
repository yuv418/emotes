from emotes.wsgi import db
from peewee import *
from playhouse.signals import pre_save, Model
import secrets

class User(db.Model):
    name = CharField()
    admin = BooleanField(default=False)

class ApiKey(Model):
    value = CharField()
    user = ForeignKeyField(User, backref="api_keys")

    class Meta:
        value = [Check('LENGTH(value) = 128')]
        database = db.database

@pre_save(sender=ApiKey)
def gen_api_key(model_class, instance, created):
    if created:
        print(f"The value before save is {instance.value}")
        instance.value = secrets.token_urlsafe(128)
    

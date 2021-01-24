from emotes.wsgi import db
from peewee import *
from playhouse.signals import pre_save, Model
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
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

    def gen_unhashed_api_key(self):
        self.value = secrets.token_urlsafe(128)
        return self.value # Convenience return

    def from_unhash(api_key):
        key = None
        keys = ApiKey.select() # get(ApiKey.value == generate_password_hash(request.values.get('api_key')))
        for i_key in keys:
            if check_password_hash(i_key.value, api_key):
                key = i_key

        return key


@pre_save(sender=ApiKey)
def gen_api_key(model_class, instance, created):
    if created:
        instance.value = generate_password_hash(instance.value)

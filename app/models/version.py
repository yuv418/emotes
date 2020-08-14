from emotes.wsgi import db
from emotes.app.models.user import *
from peewee import *

class Version(db.Model):
    version = DateTimeField()

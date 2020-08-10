from emotes.wsgi import db, app
from emotes.app.models.namespace import *
from peewee import *
from playhouse.signals import Model, pre_delete
from titlecase import titlecase
import os
import json

class Image(Model):
    """Model to keep track of resized images as part of emotes."""
    original = TextField() # Path to original image

    class Meta:
        database = db.database

class ResizedImage(Model):
    path = TextField(default=None)
    width = IntegerField()
    height = IntegerField()
    processed = BooleanField(default=False)

    image = ForeignKeyField(Image, backref='resized_images')

    class Meta:
        database = db.database

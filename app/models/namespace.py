from emotes.wsgi import db, tg, app
from emotes.app.models.user import *
from peewee import *
from playhouse.signals import post_save, Model
import traceback
import os

class Namespace(Model):

    @staticmethod
    def random_stickerpack_name():
        import uuid
        import random
        import string
        ch = string.ascii_letters + string.digits

        uid = random.choice(string.ascii_letters) + ''.join([random.choice(ch) for x in range(12)])

        return uid + "_by_" + tg.bot.get_me().username

    name = CharField()
    slug = CharField()
    parent = ForeignKeyField("self", backref='children', null=True)
    user = ForeignKeyField(User, backref='namespaces')
    tg_stickerpack_name = TextField(default=random_stickerpack_name.__func__)

    class Meta:
        database = db.database

    @staticmethod
    def from_path(path):
        if path[-1] == "/": # Remove this trailing slash
            path = path[:-1]
        namespaces = path.split("/")
        nmsp = Namespace.select().where(Namespace.slug == namespaces[0]).first()
        for nmsp_str in namespaces[1:]:
            nmsp_new = nmsp.children.select().where(Namespace.slug == nmsp_str).first()
            if not nmsp_new:
                return None
            nmsp = nmsp_new
        return nmsp

    def path(self):
        nmsp = self
        path = f'/{nmsp.slug}'
        while nmsp.parent:
            path += f"/{nmsp.parent.slug}"
            nmsp = nmsp.parent
        
        path = path.split("/")
        path.reverse()

        return '/'.join(path)



@post_save(sender=Namespace)
def create_stickerset(model, nmsp, created):
    """Create a sticker set"""
    try:
        s = tg.bot.create_new_sticker_set(
            user_id=app.config["TG_USERID"],
            name=nmsp.tg_stickerpack_name,
            title=nmsp.name,
            emojis="\N{thinking face}",
            png_sticker=open(os.path.join(app.root_path, "assets", "blank_sticker.png"), 'rb')
        )
    except Exception:
        traceback.print_exc()

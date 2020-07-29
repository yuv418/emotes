from emotes.wsgi import db
from emotes.app.models.user import *
from peewee import *

class Namespace(db.Model):
    name = CharField()
    slug = CharField()
    parent = ForeignKeyField("self", backref='children', null=True)
    user = ForeignKeyField(User, backref='namespaces')

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







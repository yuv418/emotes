from wsgi import db
from app.models.namespace import *

class Emote(db.Entity):
    path = Required(str)
    name = Required(str)
    namespace = Required(Namespace)

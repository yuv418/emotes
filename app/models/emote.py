from emotes.wsgi import db
from emotes.app.models.namespace import *
from pony.orm import *

class Emote(db.Entity):
    path = Required(str)
    name = Required(str)
    namespace = Required(Namespace)

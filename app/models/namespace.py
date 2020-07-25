from wsgi import db
from app.models.user import *

class Namespace(db.Entity):
    name = Required(str) 
    slug = Required(str)
    owners = Set(User)
    emotes = Set('Emote')





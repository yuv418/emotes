from emotes.wsgi import db
from emotes.app.models.user import *
from pony.orm import *

class Namespace(db.Entity):
    name = Required(str) 
    slug = Required(str)
    owners = Set(User)
    emotes = Set('Emote')





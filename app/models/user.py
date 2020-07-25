from emotes.wsgi import db
from pony.orm import *

class User(db.Entity):
    name = Required(str)
    namespaces = Set("Namespace")
    api_keys = Required("ApiKey")

class ApiKey(db.Entity):
    value = Required(str, 128) # == SecureRandom.alphanumeric 128
    user = Required(User)
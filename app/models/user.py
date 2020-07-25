from wsgi import db

class User(db.Entity):
    name = Required(str)
    namespaces = Set("Namespace")
    api_keys = Set("ApiKey")

class ApiKey(db.Entity):
    value = Required(str, 128) # == SecureRandom.alphanumeric 128
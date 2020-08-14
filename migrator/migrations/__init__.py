import os
from emotes.wsgi import app
import importlib

__all__ = []
migrations = os.listdir(app.config["MIGRATIONS_PATH"])
migrations = [filename[:-3] for filename in list(filter(lambda x: x.endswith(".py") and x != "__init__.py", migrations))]

for module_name in migrations:
    __all__.append(module_name)

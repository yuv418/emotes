from emotes.wsgi import app
from flask import send_from_directory
from Cheetah.Template import Template
import os

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'assets'), 'favicon.ico')

def cheetah(module, **data):
    import importlib

    classname = module.split(".")[-1]
    mod = importlib.import_module(f"emotes.app.templates.{module}")
    cls = getattr(mod, classname)

    cls_i = cls(namespaces=[data])
    return cls_i.respond()



from emotes.app.routes.api import *
from emotes.app.routes.show import *
from emotes.app.routes.ui import *

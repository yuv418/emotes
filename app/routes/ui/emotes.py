from emotes.wsgi import app, cache, ui_prefix
from emotes.app.emote import EmoteWrapper
from flask import jsonify, request, send_file, send_from_directory, render_template
from emotes.app.models import *
from emotes.app.routes import cheetah

@app.route(f"{ui_prefix}/emotes/upload")
def ui_emotes_upload():
    return cheetah("ui.upload")

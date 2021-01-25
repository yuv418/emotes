from emotes.wsgi import app, cache
from emotes.app.emote import EmoteWrapper
from flask import jsonify, request, send_file, send_from_directory, render_template
from emotes.app.models import *
from emotes.app.routes import cheetah
import os
import re
import math

@app.route("/")
def index():
    local_emotes = Emote.local_emotes()
    print(local_emotes)
    rows = math.floor(math.sqrt(len(local_emotes)))
    domain = app.config["DOMAIN"] or request.url_root

    return cheetah("ui.index", local_emotes=local_emotes, domain=domain)

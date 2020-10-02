from emotes.wsgi import app, cache
from emotes.app.emote import EmoteWrapper
from flask import jsonify, request, send_file, send_from_directory, render_template
from emotes.app.models import *
import os
import re
import math

@app.route("/")
def index():
    local_emotes = Emote.local_emotes()
    rows = math.floor(math.sqrt(len(local_emotes)))

    return render_template("ui/index.html", rows=rows, local_emotes=local_emotes)

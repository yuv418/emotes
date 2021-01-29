from emotes.wsgi import app, db, tg, api_prefix
from emotes.app.models import *
from flask import request, jsonify
from telegram import Update, InlineQueryResultCachedSticker, InputTextMessageContent, ParseMode
from uuid import uuid4

@app.route(f"{api_prefix}/tg", methods=["POST"])
def tg_webhook():
    update = Update.de_json(request.get_json(), tg.bot)
    if not update.inline_query:
        return ""

    query = update.inline_query.query
    images = None

    if query:
        nmsp = Namespace.get(Namespace.slug == query)
        if nmsp:
            images = [e.image for e in nmsp.emotes]
            print(images)
    else:
        images = Image.select().where(Image.emote_id == None)

    rszimgs = []
    for image in images:
        if image:
            if image.original.split(".")[-1] != "gif":
                rszimgs.append(image.size(256, 256, webp=1))

    results = [
      InlineQueryResultCachedSticker(
            id=uuid4(), sticker_file_id=rszimg.tg_file_id, title="z"
        ) for rszimg in rszimgs
    ]

    update.inline_query.answer(results)
    return ""

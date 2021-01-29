from emotes.wsgi import celery, app, db
from PIL import Image, ImageSequence, ImageFile
from io import BytesIO
from emotes.app.models import *
import secrets
import os
import string
import json

alphanumeric = string.ascii_letters + string.digits
ImageFile.LOAD_TRUNCATED_IMAGES = True

@celery.task()
def resize_image(resized_image_id, webp):
    """"Resizes the emote so it appears similar to a 32x32 discord emoji. Returns a BytesIO"""
    print("Started resize task.")
    from emotes.app.models.image import ResizedImage
    from peewee import InterfaceError

    resized_image_query = lambda: ResizedImage.select().where(ResizedImage.id == resized_image_id).first()
    try:
        resized_image = resized_image_query()
    except InterfaceError: # Sometimes celery disconnects from the DB after a long time and then queries fail, so we have to reconnect manually
        db.database.close()
        db.database.connect()
        resized_image = resized_image_query()

    if resized_image.image.emote_id:
        image = Image.open(os.path.join(app.config["UPLOADS_PATH"], resized_image.image.original))
    else:
        image = Image.open(resized_image.image.original)

    file_ext = resized_image.image.original.rsplit(".", 1)[1]
    emote_type = ''
    emote_name = ''

    if resized_image.image.emote_id: # For DB emotes
        emote_type = resized_image.image.emote.info['type']
        emote_name = resized_image.image.emote.name

        if emote_type == 'png': # DB hack.
            emote_type = 'emote'
        elif emote_type == 'gif':
            emote_type = 'aemote'
    else: # For local emotes
        dirname = os.path.dirname(resized_image.image.original)
        print(dirname + " is dirname")
        info_path = os.path.join(dirname, "info.json")

        emote_name = os.path.basename(os.path.dirname(dirname))

        with open(info_path) as info_f:
            info = json.load(info_f)
            emote_type = info['type']




    outfile_name = ''.join([secrets.choice(alphanumeric) for i in range(64)]) + f".{file_ext}"
    outfile_path = os.path.join(app.config["UPLOADS_PATH"], outfile_name)

    width = resized_image.width
    height = resized_image.height

    print(f"Dispatch task to resize local emote {emote_name} to size {width}x{height}")

    # Get the resize % for the image
    resize_width = width / image.width
    resize_height = height/ image.height
    resize_value = min(resize_width, resize_height)
    def __emote():

        image_resized = image.resize((int(resize_value * image.width), int(resize_value * image.height)), resample=Image.HAMMING)
        image_resized.save(outfile_path, format='PNG', quality=100)

        # Laziness, rewrite webp with composition in place.

        if webp: # Outdated. Should say 'tg' — compose emote
            import os
            from wand import image as wandimg
            with wandimg.Image(filename=outfile_path) as img_precomposite:
                img_comp = wandimg.Image(width=512, height=512)
                img_comp.composite(img_precomposite, gravity='center')
                img_comp.save(filename=outfile_path)

            # Upload sticker to telegram

            from emotes.wsgi import tg, app
            from emotes.app import models
            if resized_image.image.emote_id == None: # Local emote
                nmsp = models.Namespace.get(models.Namespace.slug == "") # Global namespace
            else:
                nmsp = resized_image.image.emote.namespace # TODO handle global emotes here

            resp = tg.bot.upload_sticker_file(
                user_id=app.config["TG_USERID"],
                png_sticker=open(outfile_path, 'rb')
            )

            print(resp)


            tg.bot.add_sticker_to_set(
                user_id=app.config["TG_USERID"],
                name=nmsp.tg_stickerpack_name,
                png_sticker=resp['file_id'],
                emojis="\N{thinking face}"
            )

            stickerset = tg.bot.get_sticker_set(name=nmsp.tg_stickerpack_name)

            for sticker in stickerset.stickers:
                # print("s", sticker)
                print("sfl", sticker.get_file())


            resized_image.tg_file_id = stickerset.stickers[-1].file_id



    def __aemote():
        # Rules to start a new image processing task:
        # The animated emote hasn't been resized yet
        # The animated emote was requested under a size that hasn't been scaled yet
        metadata = image.info

        # Extract the frames for resizing
        frames_resize = []
        for frame in ImageSequence.Iterator(image):
            frames_resize.append(frame.resize((int(resize_value * image.width), int(resize_value * image.height)), resample=Image.BOX))
        first = next(iter(frames_resize))
        first.info = metadata

        first.save(outfile_path, format='GIF', quality=100, save_all=True, append_images=frames_resize)

    switch = {
        'emote': __emote,
        'aemote': __aemote
    }
    func = switch.get(emote_type, lambda: "Cannot find type")
    func()
    print("here")

    resized_image.path = outfile_name
    resized_image.processed = True
    resized_image.webp = webp

    resized_image.save()

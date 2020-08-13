from emotes.wsgi import celery, app
from PIL import Image, ImageSequence, ImageFile
from io import BytesIO
import secrets
import os
import string

alphanumeric = string.ascii_letters + string.digits
ImageFile.LOAD_TRUNCATED_IMAGES = True

@celery.task()
def resize_image(resized_image_id):
    """"Resizes the emote so it appears similar to a 32x32 discord emoji. Returns a BytesIO"""
    from emotes.app.models.image import ResizedImage

    resized_image = ResizedImage.select().where(ResizedImage.id == resized_image_id).first()

    image = Image.open(os.path.join(app.config["UPLOADS_PATH"], resized_image.image.original))
    file_ext = resized_image.image.original.rsplit(".", 1)[1]
    emote_type = resized_image.image.emote.info['type']

    if emote_type == 'png': # DB hack.
        emote_type = 'emote'
    elif emote_type == 'gif':
        emote_type = 'aemote'

    outfile_name = ''.join([secrets.choice(alphanumeric) for i in range(64)]) + f".{file_ext}"
    outfile_path = os.path.join(app.config["UPLOADS_PATH"], outfile_name)

    width = resized_image.width
    height = resized_image.height

    print(f"Dispatch task to resize emote {resized_image.image.emote.name} to size {width}x{height}")

    # Get the resize % for the image
    resize_width = width / image.width
    resize_height = height/ image.height
    resize_value = min(resize_width, resize_height)
    def __emote():
        image_resized = image.resize((int(resize_value * image.width), int(resize_value * image.height)), resample=Image.HAMMING)

        image_resized.save(outfile_path, format='PNG', quality=100)

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

    resized_image.path = outfile_name
    resized_image.processed = True

    resized_image.save()

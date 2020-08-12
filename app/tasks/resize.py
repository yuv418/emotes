from emotes.wsgi import celery
from PIL import Image, ImageSequence
from io import BytesIO

@celery.task()
def resize_emote(emote_type, image, width, height):
    """"Resizes the emote so it appears similar to a 32x32 discord emoji. Returns a BytesIO"""

    # Get the resize % for the image
    resize_width = width / image.width
    resize_height = height/ image.height
    resize_value = min(resize_width, resize_height)
    def __emote():
        image_resized = image.resize((int(resize_value * image.width), int(resize_value * image.height)), resample=Image.HAMMING)
        i = BytesIO()
        image_resized.save(i, format='PNG', quality=100)
        i.seek(0)
        return (i, 'png')

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
        i = BytesIO()
        first.save(i, format='GIF', quality=100, save_all=True, append_images=frames_resize)
        i.seek(0)
        return (i, 'gif')
    switch = {
        'emote': __emote,
        'aemote': __aemote
    }
    func = switch.get(emote_type, lambda: "Cannot find type")

    return func()

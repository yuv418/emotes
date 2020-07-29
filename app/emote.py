from PIL import Image, ImageSequence
import os
import json
from io import BytesIO
import requests
from emotes.wsgi import app
from emotes.app.models import *

class EmoteWrapper():
    """Pull emotes from local storage, db, or api and create a nice abstraction over it"""
    
    API_PROVIDERS = ["discord", "twitch"]

    def __init__(self, namespace, emote, width, height):
        self.namespace = namespace
        self.emote = emote
        self.width = width
        self.height = height


    def fetch(self):
        """Fetch the emote from the appropriate source and return a BytesIO for returning in flask"""
        img = None
        if self.namespace == None:
            # Local
            return self.__fetch_local()

        root_namespace = self.namespace.split("/")[0]
        if root_namespace in EmoteWrapper.API_PROVIDERS:
            # API
            img = self.__fetch_api()
        else:
            # DB
            img = self.__fetch_db()
        
        #return self.__pillow_to_bytesio(self.__resize_emote(img))
        if img:
            return img
        return None

    def __resize_emote(self, image, _type):
        """"Resizes the emote so it appears similar to a 32x32 discord emoji. Returns a BytesIO"""
        
        # Get the resize % for the image
        resize_width = self.width / image.width
        resize_height = self.height/ image.height
        resize_value = min(resize_width, resize_height)
        def __emote():
            image_resized = image.resize((int(resize_value * image.width), int(resize_value * image.height)), resample=Image.HAMMING)
            i = BytesIO()
            image_resized.save(i, format='PNG', quality=100)
            i.seek(0)
            return i

        def __aemote():
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
            return i
        switch = {
            'emote': __emote,
            'aemote': __aemote
        }
        func = switch.get(_type, lambda: "Cannot find type")
        return func()

    def __pillow_to_bytesio(self, pillow_img):
        """Return a BytesIO from a Pillow so we can render stuff in Flask easily"""
        i = BytesIO()
        pillow_img.save(i, 'WEBP', quality=100)
        i.seek(0)
        return i

    def __fetch_api(self):
        """Returns a pillow image because all the post-processing is handled in fetch"""
        split = self.namespace.split("/")
        service = split[0]

        def __twitch():



        with switch as {
            'twitch': __twitch
        }:
            func = switch.get()

        # Twitch
        pass
    def __fetch_local(self):
        """
        Fetch local emotes from the emotes/* directory. 
        The __fetch_local scans that directory for 
        your given emote name (since local emotes don't have a namespace, they might later).
        
        It returns the BytesIO object for the image, resized, for easy usage within flask, like 
        all __fetch_\w+ methods.
        """

        local_emotes = os.listdir(app.config["EMOTES_PATH"])
        for emote_name in local_emotes:
            if self.emote == emote_name:
                with open(os.path.join(app.config["EMOTES_PATH"], emote_name, "info.json")) as emote_info_file:
                    emote_info = json.load(emote_info_file)
                emote_path = os.path.join(app.config["EMOTES_PATH"], emote_name, emote_info.get("path"))
                emote_type = emote_info.get("type")
                emote_pil = self.__resize_emote(Image.open(emote_path), emote_type)
                #return self.__pillow_to_bytesio(emote_pil)
                return emote_pil


        
    def __fetch_db(self):
        namespace = Namespace.from_path(self.namespace)
        if not namespace: 
            return None
        emote = namespace.emotes.select().where(Emote.slug == self.emote).first()
        if not emote:
            return None

        emote_pil = Image.open(os.path.join(app.config["UPLOADS_PATH"], emote.path))
        emote_type = "emote"
        if emote.path.rsplit(".", 1)[1] == "gif":
            emote_type = "aemote"

        return self.__resize_emote(emote_pil, emote_type)

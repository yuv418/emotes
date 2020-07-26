from PIL import Image
import os
import json
from io import BytesIO
import requests

class EmoteWrapper():
    """Pull emotes from local storage, db, or api and create a nice abstraction over it"""

    API_PROVIDERS = ["discord", "twitch"] # TODO slack
    
    def __init__(self, namespace, emote, width, height):
        self.namespace = namespace
        self.emote = emote
        self.width = width
        self.height = height


    def fetch(self):
        """Fetch the emote from the appropriate source and return a BytesIO for returning in flask"""
        if self.namespace == None:
            # Local
            return self.__fetch_local()

        root_namespace = self.namespace.split("/")[0]
        if root_namespace in API_PROVIDERS:
            # API
            return self.__fetch_api()
        else:
            # DB
            return self.__fetch_db()

    def __resize_emote(self, path):
        image = Image.open(path)
        resize_width = self.width / image.width
        resize_height = self.height/ image.height
        resize_value = min(resize_width, resize_height)
        image_resize = image.resize((int(resize_value * image.width), int(resize_value * image.height)), resample=Image.HAMMING)
        return image_resize

    def __pillow_to_bytesio(self, pillow_img):
        """Return a BytesIO from a Pillow so we can render stuff in Flask easily"""
        i = BytesIO()
        pillow_img.save(i, 'PNG', quality=100)
        i.seek(0)
        return i

    def __fetch_api(self):
        split = self.namespace.split("/")
        service = split[0]
        guild = split[1]
        emoteId = spliet[2]
        if service == 'discord':
            data = {
                'client_id': app.config['DISCORD_ID'],
                'client_secret': app.config['DISCORD_SECRET'],
                'grant_type': 'authorization_code',
                'redirect_uri': app.config['REDIRECT_URI'],
                'scope': 'guilds'
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            r = request.post(f'{app.config["DISCORD_ENDPOINT"]}/oauth2/token', data=data, headers=headers)
            print(r.status_code)
            pass
        pass
    def __fetch_local(self):
        """
        Fetch local emotes from the emotes/* directory. 
        The __fetch_local scans that directory for 
        your given emote name (since local emotes don't have a namespace, they might later).
        
        It returns the BytesIO object for the image, resized, for easy usage within flask, like 
        all __fetch_\w+ methods.
        """

        local_emotes = os.listdir(os.path.join(os.getcwd(), "emotes"))
        for emote_name in local_emotes:
            if self.emote == emote_name:
                with open(os.path.join(os.getcwd(), "emotes", emote_name, "info.json")) as emote_info_file:
                    emote_info = json.load(emote_info_file)
                emote_path = os.path.join(os.getcwd(), "emotes", emote_name, emote_info.get("path"))
                emote_pil = self.__resize_emote(emote_path)
                return self.__pillow_to_bytesio(emote_pil)


        
    def __fetch_db(self):
        pass

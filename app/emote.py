from PIL import Image

class EmoteWrapper():
    """Pull emotes from local storage, db, or api and create a nice abstraction over it"""
    
    def __init__(self, namespace, emote, width, height):
        self.namespace = namespace
        self.emote = emote
        self.width = width
        self.height = height

    def resize_emote(self, path):
        image = Image.open(path)
        resizeWidth = self.width / image.width
        resizeHeight = self.height/ image.height
        resizeValue = min(resizeWidth, resizeHeight)
        imageResize = image.resize((resizeValue * image.width, resizeValue * image.height)), resample=Image.HAMMING)
        return imageResize
    def fetch_api(self):
        pass
    def fetch_local(self):
        pass
    def fetch_db(self):
        pass

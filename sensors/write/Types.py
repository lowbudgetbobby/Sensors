class ImageWriteObject:
    def __init__(self, img, resize=None, name='default'):
        self.img = img
        self.resize = resize
        self.name = name
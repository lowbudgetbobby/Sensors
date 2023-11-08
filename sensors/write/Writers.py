import cv2
from sensors.write.Handlers import ImageToDesktopHandler
from sensors.write.Types import ImageWriteObject


class Writer:
    fields = []
    handle = None
    handle_class = None

    def __init__(self, handle_class=None):
        self.handle_class = handle_class

    def do_write(self, data):
        Exception('do_write must be over written.')


class ImageWriter(Writer):
    handle_class = ImageToDesktopHandler

    def __init__(self, handle_class=ImageToDesktopHandler):
        super().__init__(handle_class)

    def do_write(self, data: ImageWriteObject):
        if self.handle is None:
            self.handle = self.handle_class()

        if data.size is not None:
            img = cv2.resize(data.img, data.size)
        else:
            img = data.img

        return self.handle.write(
            img, data.text
        )

import cv2
from sensors.write.Handlers import ImageToDesktopHandler
from sensors.write.Types import ImageWriteObject


class Writer:
    fields = []
    _handle = None
    handle_class = None

    def __init__(self, handle_class=None):
        self.handle_class = handle_class

    @property
    def handle(self):
        if self._handle is None:
            self._handle = self.handle_class()
        return self._handle

    def do_write(self, data):
        Exception('do_write must be over written.')


class ImageWriter(Writer):
    handle_class = ImageToDesktopHandler

    def __init__(self, handle_class=ImageToDesktopHandler):
        super().__init__(handle_class)

    def do_write(self, data: ImageWriteObject):
        if data.size is not None:
            img = cv2.resize(data.img, data.size)
        else:
            img = data.img

        return self.handle.write(
            img, data.text
        )

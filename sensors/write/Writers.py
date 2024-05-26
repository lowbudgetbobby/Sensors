from sensors.write.Handlers import ImageToDesktopHandler, StartStopButtonHandler
from sensors.write.Types import ImageWriteObject
from sensors.readerwriterbase import ReaderWriter, HandleBase


class Writer(ReaderWriter):
    def do_write(self, *args, **kwargs):
        self.do_readwrite(*args, **kwargs)
        if self.error is not None:
            return False, self.error

        return self.data, None

    def do(self, *args, **kwargs):
        return self.handle.write(*args, **kwargs)


class ImageWriter(Writer):
    def __init__(self, handler: HandleBase = ImageToDesktopHandler()):
        super().__init__(handler)

    def do(self, data: ImageWriteObject, *args, **kwargs):
        if data.size is not None:
            img = self.handle.resize(data.img, data.size)
        else:
            img = data.img

        return self.handle.write(
            img, data.text
        )


class StartStopButtonReader(Writer):
    def __init__(self, handler: HandleBase = StartStopButtonHandler()):
        super().__init__(
            handler
        )

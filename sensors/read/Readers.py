from sensors.read.Handlers import (RandomHandler, TiltSensorHandler,
                                   KeyboardHandler, CameraHandler, FileHandler,
                                   NullHandler)
from sensors.readerwriterbase import ReaderWriter, HandleBase
import os
import numpy as np

directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)


class Reader(ReaderWriter):

    def do_read(self):
        self.do_readwrite()
        if self.error is not None:
            return None, self.error
        return self.data, None

    def do(self, *args, **kwargs):
        return self.handle.read()

    def dump(self):
        self.data = None


class ReaderCollection(Reader):
    def __init__(self, readers: list[Reader]):
        super().__init__(NullHandler())
        self.readers = readers

    def do(self, *args, **kwargs):
        data = []
        for reader in self.readers:
            reader.do()
            data.append(reader.data)

        return data

    def dump(self):
        self.data = None
        for reader in self.readers:
            reader.dump()


class FileReader(Reader):
    def __init__(self, file):
        super().__init__(FileHandler(file))

    def do(self, *args, **kwargs):
        out = self.handle.read()
        if out == '':
            self.handle.stop()
            raise Exception('End of file reached.')

        if not self.data:
            self.data = ''

        self.data += out
        return self.data


class RandomReader(Reader):
    def __init__(self, handler: HandleBase = RandomHandler()):
        super().__init__(
            handler
        )

    def do(self, *args, **kwargs):
        num = self.handle.read()
        if not self.data:
            self.data = [num, 1]
        else:
            self.data[0] += num
            self.data[1] += 1

        return self.data


class TiltSensorReader(Reader):
    def __init__(self, handler: HandleBase = TiltSensorHandler()):
        super().__init__(
            handler
        )

    def do(self, *args, **kwargs):
        new_data = self.handle.read() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data

        return self.data


class KeyboardReader(Reader):
    def __init__(self, handler: HandleBase = KeyboardHandler()):
        super().__init__(
            handler
        )

    def do(self, *args, **kwargs):
        new_data = self.handle.read() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data

        return self.data


class CameraReader(Reader):
    def __init__(self, handler: HandleBase = CameraHandler()):
        super().__init__(
            handler
        )


class ExposureCameraReader(CameraReader):

    def __init__(self, sampling, handler: HandleBase = CameraHandler()):
        super().__init__(handler)
        self.sampling = sampling
        self.frames = []

    def do(self, *args, **kwargs):
        img = self.handle.read()
        if img is None:
            return None

        self.frames.append(img)
        if len(self.frames) > self.sampling:
            self.frames.pop(0)

        div = len(self.frames)
        f = None
        for frame in self.frames:
            if f is None:
                f = frame / div
            else:
                f += frame / div
        self.data = np.asarray(f, dtype=np.uint8)

        return self.data

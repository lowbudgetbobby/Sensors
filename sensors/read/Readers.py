from sensors.read.Handlers import RandomHandler, TiltSensorHandler, KeyboardHandler, CameraHandler, StartStopButtonHandler
import platform
import os
import numpy as np

if platform.uname().node == 'raspberrypi':
    from sensors.read.Handlers import FPSCameraHandler

directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)


class Reader:
    data = None
    _handle = None
    handle_class = None

    def __init__(self, handle_class=None):
        self.handle_class = handle_class or self.handle_class

    @property
    def handle(self):
        if self._handle is None:
            self._handle = self.handle_class()
        return self._handle

    def do_read(self):
        self.data = self.handle.get()

    def dump(self):
        self.data = None


class ReaderCollection(Reader):
    def __init__(self, readers: list[Reader]):
        self.readers = readers

    def do_read(self):
        self.data = []
        for reader in self.readers:
            reader.do_read()
            self.data.append(reader.data)

    def dump(self):
        self.data = None
        for reader in self.readers:
            reader.dump()


class FileReader(Reader):
    def __init__(self, file):
        self.file = file
        self._handle = open(self.file, "r")

    def do_read(self):
        out = self.handle.readline().rstrip()
        if out == '':
            self.handle.close()
            raise Exception('End of file reached.')

        if not self.data:
            self.data = ''

        self.data += out


class RandomReader(Reader):
    handle_class = RandomHandler

    def do_read(self):
        num = self.handle.get()
        if not self.data:
            self.data = [num, 1]
        else:
            self.data[0] += num
            self.data[1] += 1


class TiltSensorReader(Reader):
    handle_class = TiltSensorHandler

    def do_read(self):
        new_data = self.handle.get() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data


class KeyboardReader(Reader):
    handle_class = KeyboardHandler

    def do_read(self):
        new_data = self.handle.get() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data


class CameraReader(Reader):
    handle_class = CameraHandler


class ExposureCameraReader(CameraReader):

    def __init__(self, sampling, handle_class=None):
        super().__init__(handle_class)
        self.sampling = sampling
        self.frames = []

    def do_read(self):
        img = self.handle.get()
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

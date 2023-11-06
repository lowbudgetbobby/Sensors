from sensors.read.Handlers import RandomHandler, TiltSensorHandler, KeyboardHandler, CameraHandler, StartStopButtonHandler
import platform
import os
import numpy as np

if platform.uname().node == 'raspberrypi':
    from sensors.read.Handlers import RaspPiCameraHandler

directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)


class Reader:
    data = None
    handle = None

    def do_read(self):
        Exception('_do_read must be over written.')

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
    file = None

    def __init__(self, file):
        self.file = file

    def do_read(self):
        if not self.handle:
            self.handle = open(self.file, "r")

        out = self.handle.readline().rstrip()
        if out == '':
            self.handle.close()
            raise Exception('End of file reached.')

        if not self.data:
            self.data = ''

        self.data += out


class RandomReader(Reader):

    def __init__(self):
        self.handler = RandomHandler()

    def do_read(self):
        num = self.handler.get()
        if not self.data:
            self.data = [num, 1]
        else:
            self.data[0] += num
            self.data[1] += 1


class TiltSensorReader(Reader):

    def __init__(self):
        self.handle = TiltSensorHandler()

    def do_read(self):
        new_data = self.handle.get_delta_angles() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data


class KeyboardReader(Reader):

    def __init__(self):
        self.handle = KeyboardHandler()

    def do_read(self):
        new_data = self.handle.get() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data


class CameraReader(Reader):

    def __init__(self):
        self.handle = None

    def do_read(self):
        if not self.handle:
            self.handle = CameraHandler()

        self.data = self.handle.get()


class ExposureCameraReader(CameraReader):

    def __init__(self, sampling):
        super().__init__()
        self.sampling = sampling
        self.frames = []

    def do_read(self):
        if not self.handle:
            self.handle = CameraHandler()

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


if platform.uname().node == 'raspberrypi':
    class RaspPiCameraReader(Reader):

        def __init__(self):
            self.handle = None

        def do_read(self):
            if not self.handle:
                self.handle = RaspPiCameraHandler()
                self.handle.start_stream()

            self.data = self.handle.get()


    class StartStopButtonReader(Reader):

        def __init__(self):
            self.handle = None

        def do_read(self):
            if not self.handle:
                self.handle = StartStopButtonHandler()

            self.data = self.handle.read()

from .handlers import RandomHandler, TiltSensorHandler, KeyboardHandler, CameraHandler
import platform
import os

if platform.uname().node == 'raspberrypi':
    from .handlers import RaspPiCameraHandler

directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)


class Reader:
    name = 'reader'
    data = None
    handle = None

    def do_read(self):
        Exception('_do_read must be over written.')

    def dump(self):
        self.data = None


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


if platform.uname().node == 'raspberrypi':
    class RaspPiCameraReader(Reader):

        def __init__(self):
            self.handle = RaspPiCameraHandler()
            self.handle.start_stream()

        def do_read(self):
            self.data = self.handle.get()

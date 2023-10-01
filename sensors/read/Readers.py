from .handlers import RandomHandler, TiltSensorHandler, KeyboardHandler, CameraHandler
import os

directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)


class Reader:
    name = 'reader'
    read_rate = 0
    data = None
    handle = None

    def __init__(self, read_rate):
        self.read_rate = read_rate

    def read(self):
        while True:
            if os.path.isfile(f"{parent_dir}/flag_files/.clear-{self.name}"):
                try:
                    os.remove(f"{parent_dir}/flag_files/.clear-{self.name}")
                    self.dump()
                except Exception:
                    pass

            self._do_read()
            yield self.data
            # time.sleep(self.read_rate)

    def _do_read(self):
        Exception('_do_read must be over written.')

    def dump(self):
        self.data = None


class FileReader(Reader):
    name = 'file-reader'
    file = None

    def __init__(self, read_rate, file):
        super().__init__(read_rate)
        self.file = file

    def _do_read(self):
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
    name = 'random-reader'

    def _do_read(self):
        if not self.handle:
            self.handler = RandomHandler()

        num = self.handler.get()
        if not self.data:
            self.data = [num, 1]
        else:
            self.data[0] += num
            self.data[1] += 1


class TiltSensorReader(Reader):
    name = 'tilt-reader'

    def _do_read(self):
        if not self.handle:
            self.handle = TiltSensorHandler()

        new_data = self.handle.get_delta_angles() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data


class KeyboardReader(Reader):
    name = 'keyboard-reader'

    def _do_read(self):
        if not self.handle:
            self.handle = KeyboardHandler()

        new_data = self.handle.get() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data


class CameraReader(Reader):
    name = 'camera-reader'

    def _do_read(self):
        if not self.handle:
            self.handle = CameraHandler()

        self.data = self.handle.get()

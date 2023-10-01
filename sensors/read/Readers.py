import time
import sys
from read.handlers import RandomHandler, TiltSensorHandler, KeyboardHandler
import os
import json

directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)


class Reader:
    read_rate = 0
    data = None
    handle = None

    def __init__(self, read_rate):
        self.read_rate = read_rate

    def read(self):
        while True:
            if os.path.isfile(f"{parent_dir}/flag_files/.clear"):
                os.remove(f"{parent_dir}/flag_files/.clear")
                self.dump()

            self._do_read()
            yield json.dumps(self.data)
            time.sleep(self.read_rate)

    def _do_read(self):
        Exception('_do_read must be over written.')

    def dump(self):
        self.data = None


class FileReader(Reader):
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
    comp = None

    def _do_read(self):
        if not self.handle:
            self.handler = RandomHandler()

        num = self.handler.get()
        if not self.comp:
            self.comp = [num, 1]
        else:
            self.comp[0] += num
            self.comp[1] += 1

        self.data = self.comp


class TiltSensorReader(Reader):

    def _do_read(self):
        if not self.handle:
            self.handle = TiltSensorHandler()

        new_data = self.handle.get_delta_angles() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data

    def dump(self):
        self.data = None


class KeyboardReader(Reader):

    def _do_read(self):
        if not self.handle:
            self.handle = KeyboardHandler()

        new_data = self.handle.get() + [1]
        if self.data:
            for i in range(0, len(new_data)):
                self.data[i] += new_data[i]
        else:
            self.data = new_data

    def dump(self):
        self.data = None

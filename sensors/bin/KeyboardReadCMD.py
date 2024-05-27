import sys
import os
import cv2
import time

from sensors.read.Readers import KeyboardReader
from sensors.read.Manager import ManageRead


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0) # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))
    m = ManageRead(
        KeyboardReader()
    )

    m.runProc()
    while True:
        data = m.readProc()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(data)

        time.sleep(read_rate)

    sys.exit(0)

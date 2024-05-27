import sys
import os
import cv2
import time

from sensors.read.Readers import CameraReader
from sensors.read.Manager import ManageRead
from sensors.write.Writers import ImageWriter
from sensors.write.Manager import ManageWriter
from sensors.read.Readers import Reader
from sensors.read.Handlers import QuitKeyboardHandler
from sensors.write.Types import ImageWriteObject


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0)  # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))
    m = ManageRead(
            CameraReader()
    )

    q = ManageRead(
        Reader(
            QuitKeyboardHandler()
        )
    )

    w = ManageWriter(
        ImageWriter()
    )

    m.runProc()
    q.runProc()
    w.runProc()

    q_state = q.readProc()
    while not q_state:
        data = m.readProc(False)
        q_state = q.readProc()

        if data is not None:
            w.writeProc(
                ImageWriteObject(data)
            )
        else:
            print("dropped frame.")

        time.sleep(read_rate)

    m.stopProc()
    q.stopProc()
    w.stopProc()
    print('Key interupt. Stopping stream.')

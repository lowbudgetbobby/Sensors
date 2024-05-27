import sys
import os
import cv2
import time

from sensors.read.Readers import CameraReader
from sensors.read.Manager import ManageRead
from sensors.write.Writers import ImageWriter
from sensors.write.Manager import ManageWriter
from sensors.write.Types import ImageWriteObject


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0)  # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))
    m = ManageRead(
            CameraReader()
    )

    w = ManageWriter(
        ImageWriter()
    )

    m.runProc()
    w.runProc()
    while True:
        data = m.readProc(False)

        if data is not None:
            w.writeProc(
                ImageWriteObject(data)
            )
        else:
            print("dropped frame.")


        time.sleep(read_rate)

    sys.exit(1)

import sys
import os
import cv2
import time

directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(directory)
sys.path.append(parent)

from read.Readers import CameraReader
from read.Manager import ManageRead
from write.Writers import ImageWriter
from write.Manager import ManageWriter
from write.Types import ImageWriteObject


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0) # get rid of the first argument, it's this file's name.
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

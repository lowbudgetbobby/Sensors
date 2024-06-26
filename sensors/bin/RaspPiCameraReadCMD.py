import sys
import os
import cv2
import time

from sensors.read.Handlers import PiCameraHandler
from sensors.read.Readers import CameraReader
from sensors.read.Manager import ManageRead
import platform

if platform.uname().node != 'raspberrypi':
    exit()

if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0) # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))
    m = ManageRead(
            CameraReader(
                PiCameraHandler()
            )
    )

    m.runProc()
    while True:
        data = m.readProc(False)

        if data is not None:
            cv2.imshow("Demo", data)
        else:
            print("dropped frame.")
        k = cv2.waitKey(1)
        if k == 27:
            break

        time.sleep(read_rate)

    cv2.destroyAllWindows()

    sys.exit(1)

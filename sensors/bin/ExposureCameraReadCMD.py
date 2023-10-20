import sys
import os
import cv2
import time

directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(directory)
sys.path.append(parent)

from read.Readers import ExposureCameraReader
from read.Manager import ManageRead


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0) # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))
    m = ManageRead(
            ExposureCameraReader(4)
    )

    m.runProc()
    while True:
        data = m.readProc(True, False)
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

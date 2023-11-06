import sys
import os
import time

directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(directory)
sys.path.append(parent)

from read.Readers import StartStopButtonReader
from read.Manager import ManageRead


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0) # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))
    m = ManageRead(
            StartStopButtonReader()
    )

    m.runProc()
    while True:
        data = m.readProc(False)
        print(data)

        time.sleep(read_rate)

    cv2.destroyAllWindows()

    sys.exit(1)

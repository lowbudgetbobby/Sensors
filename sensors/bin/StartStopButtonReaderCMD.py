import sys
import os
import time

from sensors.read.Readers import Reader
from sensors.read.Handlers import StateButtonHandler
from sensors.read.Manager import ManageRead


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0) # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))
    m = ManageRead(
        Reader(
            StateButtonHandler()
        )
    )

    m.runProc()
    while True:
        data = m.readProc(False)
        print(data)

        time.sleep(read_rate)

    cv2.destroyAllWindows()

    sys.exit(1)

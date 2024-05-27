import sys
import os
import time

from sensors.read.Readers import TiltSensorReader
from sensors.read.Manager import ManageRead


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0) # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))

    m = ManageRead(
        TiltSensorReader()
    )

    m.runProc()
    while True:
        data = m.readProc()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(
            '%.4f | %.4f | %.4f' % (data[0] / data[3], data[1] / data[3], data[2] / data[3])
        )
        time.sleep(read_rate)

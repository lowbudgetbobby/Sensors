import sys
import os

from sensors.read.Readers import RandomReader
from sensors.read.Manager import ManageRead

import time


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0) # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))

    m = ManageRead(
        RandomReader()
    )

    m.runProc()
    if read_rate:
        while True:
            data = m.readProc()
            os.system('cls' if os.name == 'nt' else 'clear')
            print(data)
            time.sleep(read_rate)
        sys.exit(0)

    sys.exit(1)

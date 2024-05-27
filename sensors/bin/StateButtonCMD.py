import sys
import time

from sensors.read.Manager import ManageRead
from sensors.read.Readers import Reader
from sensors.read.Handlers import StateButtonHandler as StateButtonHandler_READ
from sensors.write.Handlers import StateButtonHandler as StateButtonHandler_WRITE
from sensors.write.Writers import Writer
from sensors.write.Manager import ManageWriter


if __name__ == '__main__':
    args = list(sys.argv)
    args.pop(0)  # get rid of the first argument, it's this file's name.
    read_rate = float(args.pop(0))

    state_check_proc = ManageRead(
        Reader(
            StateButtonHandler_READ()
        )
    )
    state_write_proc = ManageWriter(
        Writer(
            StateButtonHandler_WRITE()
        )
    )

    state_check_proc.runProc()
    state_write_proc.runProc()

    count_lim = 3
    curr_count = 0
    while True:
        if curr_count == count_lim:
            curr_count = 0
            state_write_proc.writeProc(1)
        else:
            curr_count += 1
            print(state_check_proc.readProc(False))

        time.sleep(read_rate)

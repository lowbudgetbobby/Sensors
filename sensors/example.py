from read.Manager import ManageRead
from read.Readers import RandomReader, TiltSensorReader, KeyboardReader
import time

if __name__ == '__main__':
    m = ManageRead(
        KeyboardReader(0.1)
    )
    m.runProc()
    while True:
        out = m.readProc()
        print(out)
        time.sleep(1)

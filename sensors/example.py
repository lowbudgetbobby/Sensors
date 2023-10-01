from read.Manager import ManageRead
from read.Readers import RandomReader, TiltSensorReader
import time

if __name__ == '__main__':
    m = ManageRead(
        TiltSensorReader(0)
    )
    m.runProc()
    while True:
        out = m.readProc()
        print(
            '%s | %s | %s' % (out[0] * (0.1/out[3]), out[1] * (0.1/out[3]), out[2] * (0.1/out[3]))
        )
        time.sleep(0.1)

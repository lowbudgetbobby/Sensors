from read.Manager import ManageRead
from read.Readers import TiltSensorReader
import time

if __name__ == '__main__':
    m = ManageRead(
        TiltSensorReader(0)
    )
    m.runProc()
    time.sleep(30)
    out = m.readProc()
    print(
        out
    )
    print(
        float(out[0]) / float(out[3])
    )
    print(
        float(out[1]) / float(out[3])
    )
    print(
        float(out[2]) / float(out[3])
    )

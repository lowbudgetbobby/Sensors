from read.Manager import ManageRead
from read.Readers import TiltSensorReader
import time

if __name__ == '__main__':
    m = ManageRead(
        TiltSensorReader()
    )
    m.runProc()
    data = m.readProc()
    for i in range(0, 10000):
        newData = m.readProc()
        for j in range(0, len(newData)):
            data[j] += newData[j]
    out = data
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

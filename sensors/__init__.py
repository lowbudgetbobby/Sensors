from .read.Manager import ManageRead
from .read.Readers import KeyboardReader, TiltSensorReader, CameraReader

def TiltSensor(read_rate):
    return ManageRead(
        TiltSensorReader(read_rate)
    )

def KeyboardSensor(read_rate):
    return ManageRead(
        KeyboardReader(read_rate)
    )

def CameraSensor(read_rate):
    return ManageRead(
        CameraReader(read_rate)
    )

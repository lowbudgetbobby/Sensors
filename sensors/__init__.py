from .read.Manager import ManageRead
from .read.Readers import KeyboardReader, TiltSensorReader, CameraReader, RaspPiCameraReader


def TiltSensor():
    return ManageRead(
        TiltSensorReader()
    )


def KeyboardSensor():
    return ManageRead(
        KeyboardReader()
    )


def CameraSensor():
    return ManageRead(
        CameraReader()
    )


def RaspPiCameraSensor():
    return ManageRead(
        RaspPiCameraReader()
    )

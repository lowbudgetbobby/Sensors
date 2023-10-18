from .read.Manager import ManageRead
from .read.Readers import KeyboardReader, TiltSensorReader, CameraReader
import platform


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


if platform.uname().node == 'raspberrypi':
    from .read.Readers import RaspPiCameraReader

    def RaspPiCameraSensor():
        return ManageRead(
            RaspPiCameraReader()
        )

import sys
import os

directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(directory)
sys.path.append(parent)

from utils.kalman import Tracker


class TiltSensorAnglesDelta:
    roll = 0
    pitch = 0
    yaw = 0

    rollFilter = None
    pitchFilter = None
    yawFilter = None

    def __init__(
        self,
    ):
        self.rollFilter = Tracker('gyroX', 0)
        self.pitchFilter = Tracker('gyroY', 0)
        self.yawFilter = Tracker('gyroZ', 0)

    def update(
        self,
        gyroX,
        gyroY,
        gyroZ
    ):
        newRoll = gyroX
        newPitch = gyroY
        newYaw = gyroZ

        self.rollFilter.update(newRoll)
        self.pitchFilter.update(newPitch)
        self.yawFilter.update(newYaw)

        self.roll = self.rollFilter.get()
        self.pitch = self.pitchFilter.get()
        self.yaw = self.yawFilter.get()

    def serialize(self):
        return [self.roll, self.pitch, self.yaw]

import cv2
import numpy as np

class Tracker():
    """Using Kalman filter as a point stabilizer."""

    def __init__(self,
                 id,
                 point,
                 cov_process=0.03,
                 cov_measure=0.1):
        self.id = id

        # The filter itself.
        self.kalman = cv2.KalmanFilter(2, 1)

        # Kalman parameters setup for scalar.
        self.kalman.transitionMatrix = np.array([[1, 1],
                                                 [0, 1]], np.float32)

        self.kalman.measurementMatrix = np.array([[1, 1]], np.float32)

        self.kalman.processNoiseCov = np.array([[1, 0],
                                                [0, 1]], np.float32) * cov_process

        self.kalman.measurementNoiseCov = np.array([[1]], np.float32) * cov_measure

        self.kalman.statePre = np.array([[point], [0]], np.float32)
        self.kalman.statePost = np.array([[point], [0]], np.float32)

    def update(self, measurement):
        """Update the filter"""
        # Make kalman prediction
        self.kalman.predict()

        # Get new measurement
        measurement = np.array([[np.float32(measurement)]])

        # Correct according to mesurement
        self.kalman.correct(measurement)

    def get(self):
        point, _ = self.kalman.statePost
        return float(point)

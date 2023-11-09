import random
import platform
import keyboard
import cv2
import numpy
from .Types import TiltSensorAnglesDelta

is_raspberrypi = False
try:
    if platform.uname().node == 'raspberrypi':
        import RPi.GPIO as GPIO
        import smbus
        is_raspberrypi = True
except Exception:
    pass

if is_raspberrypi:
    # Taken and addapted from: https://srituhobby.com/how-to-use-the-mpu6050-sensor-module-with-raspberry-pi-board/?wmc-currency=EUR
    # This can only run on a Raspberry Pi.

    # Setup GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #some MPU6050 Registers and their Address
    PWR_MGMT_1   = 0x6B
    SMPLRT_DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    INT_ENABLE   = 0x38
    ACCEL_XOUT = 0x3B
    ACCEL_YOUT = 0x3D
    ACCEL_ZOUT = 0x3F
    GYRO_XOUT  = 0x43
    GYRO_YOUT  = 0x45
    GYRO_ZOUT  = 0x47

    ROLL_OFFSET = -0.3419891147334961
    PITCH_OFFSET = 0.0493546505654258
    YAW_OFFSET = -0.015088877203797183

    class TiltSensorHandler:
        bus = None
        Device_Address = 0x68  # MPU6050 device address
        state = None

        def __init__(self):
            self.MPU_Init()
            self.state = TiltSensorAnglesDelta()

        def MPU_Init(self):
            self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards


            # write to sample rate register
            self.bus.write_byte_data(self.Device_Address, SMPLRT_DIV, 7)

            # Write to power management register
            self.bus.write_byte_data(self.Device_Address, PWR_MGMT_1, 1)

            # Write to Configuration register
            self.bus.write_byte_data(self.Device_Address, CONFIG, int('0000110', 2))

            # Write to Gyro configuration register
            self.bus.write_byte_data(self.Device_Address, GYRO_CONFIG, 24)

            # Write to interrupt enable register
            self.bus.write_byte_data(self.Device_Address, INT_ENABLE, 1)

        def read_raw_data(self, addr):
            # Accelero and Gyro value are 16-bit
            high = self.bus.read_byte_data(self.Device_Address, addr)
            low = self.bus.read_byte_data(self.Device_Address, addr + 1)

            # concatenate higher and lower value
            value = ((high << 8) | low)

            # to get signed value from mpu6050
            if (value > 32768):
                value = value - 65536
            return value

        def get_delta_angles(self):
            # Read Gyroscope raw value
            gyroX = self.read_raw_data(GYRO_XOUT)/131.0 - ROLL_OFFSET
            gyroY = self.read_raw_data(GYRO_YOUT)/131.0 - PITCH_OFFSET
            gyroZ = self.read_raw_data(GYRO_ZOUT)/131.0 - YAW_OFFSET

            self.state.update(gyroX, gyroY, gyroZ)

            return self.state.serialize()

        def get(self):
            return self.get_delta_angles()


    READ_STATE_PIN = 5
    # WRITE_START_PIN = 6
    WRITE_RESET_PIN = 13

    class StartStopButtonHandler:
        def __init__(self):
            self._init_mem()
            self.reset()

        def _init_mem(self):
            GPIO.setup(READ_STATE_PIN, GPIO.IN)
            GPIO.setup(WRITE_RESET_PIN, GPIO.OUT)

        def reset(self):
            GPIO.output(WRITE_RESET_PIN, GPIO.HIGH)
            GPIO.output(WRITE_RESET_PIN, GPIO.LOW)

        def read(self):
            return GPIO.input(READ_STATE_PIN)

        def get(self):
            return self.read()

        def cleanup(self):
            GPIO.cleanup()


    from imutils.video import VideoStream, FPS
    class FPSCameraHandler:
        vs = None
        fps = None

        def __init__(self):
            self.vs = VideoStream(src=0, usePiCamera=True)
            self.fps = FPS()
            self.start_stream()

        def start_stream(self):
            self.vs.start()
            self.fps.start()

        def get(self):
            try:
                frame = self.vs.read()
                self.fps.update()
                return frame
            except:
                return None

        def stop_stream(self):
            self.fps.stop()
            self.vs.stop()


    from picamera import PiCamera
    from io import BytesIO
    class PiCameraHandler:
        camera = None
        format = None

        def __init__(self, format='jpeg'):
            self.camera = PiCamera()
            self.format = format

        def get(self):
            stream = BytesIO()
            self.camera.capture(stream, format=self.format)
            stream.seek(0)

            return stream

else:
    class TiltSensorHandler:
        def get(self):
            pass

    class StartStopButtonHandler:
        def get(self):
            pass


class RandomHandler:
    def get(self):
        return random.randint(-5, 5)


class KeyboardHandler:
    units = 0.1

    def get(self):
        ret = [0,0]
        if keyboard.is_pressed("a"):
            ret[0] = self.units
        elif keyboard.is_pressed("d"):
            ret[0] = -self.units

        if keyboard.is_pressed("w"):
            ret[1] = self.units
        elif keyboard.is_pressed("s"):
            ret[1] = -self.units

        return ret


class CameraHandler:
    def __init__(self):
        self.webcam = cv2.VideoCapture(0)
        self.frame_size = (
            self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH),
            self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

    def get(self):
        # We get a new frame from the webcam
        _, frame = self.webcam.read()
        if type(frame).__module__ == numpy.__name__:
            return frame
        else:
            return None

    def close(self):
        self.webcam.release()
        cv2.destroyAllWindows()

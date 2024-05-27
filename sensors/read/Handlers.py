import random
import platform
import numpy
from .Types import TiltSensorAnglesDelta
from sensors.readerwriterbase import HandleBase, StateButtonHandlerBase

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

    class TiltSensorHandler(HandleBase):
        bus = None
        Device_Address = 0x68  # MPU6050 device address
        state = None

        def start(self):
            self.MPU_Init()
            self.state = TiltSensorAnglesDelta()
            self.is_running = True

        def stop(self):
            self.require_running()
            self.is_running = False

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

        def read(self):
            self.require_running()
            return self.get_delta_angles()


    READ_STATE_PIN = 5

    class StateButtonHandler(StateButtonHandlerBase):
        def read(self):
            self.require_running()
            return GPIO.input(READ_STATE_PIN)


    from picamera import PiCamera
    from io import BytesIO
    class PiCameraHandler(HandleBase):
        camera = None
        format = None
        stream = None
        rawCapture = None

        def __init__(self, format='jpeg', resolution=None, framerate=None):
            self.format = format
            self.resolution = resolution
            self.framerate = framerate

        def start(self):
            self.camera = PiCamera()
            if self.resolution is not None:
                self.camera.resolution = self.resolution
            if self.framerate is not None:
                self.camera.framerate = self.framerate

            self.rawCapture = BytesIO()
            self.stream = self.camera.capture_continuous(
                self.rawCapture,
                format=self.format,
                use_video_port=True
            )
            self.is_running = True

        def read(self):
            self.require_running()
            if next(self.stream):
                self.rawCapture.seek(0)
                imgBytes = self.rawCapture.read()
                self.rawCapture.seek(0)
                self.rawCapture.truncate()
                if len(imgBytes) == 0:
                    return None

                return imgBytes
            else:
                return None

        def stop(self):
            self.require_running()
            self.stream.close()
            self.rawCapture.close()
            self.camera.close()
            self.is_running = False


    class KeyboardHandler(HandleBase):
        def read(self):
            pass


    class CameraHandler(HandleBase):
        def read(self):
            pass

else:
    class TiltSensorHandler(HandleBase):
        def read(self):
            pass


    class StateButtonHandler(StateButtonHandlerBase):
        def read(self):
            pass


    import keyboard
    class KeyboardHandler(HandleBase):
        is_running = True
        units = 0.1

        def start(self):
            pass

        def stop(self):
            pass

        def read(self):
            ret = [0, 0]
            if keyboard.is_pressed("a"):
                ret[0] = self.units
            elif keyboard.is_pressed("d"):
                ret[0] = -self.units

            if keyboard.is_pressed("w"):
                ret[1] = self.units
            elif keyboard.is_pressed("s"):
                ret[1] = -self.units

            return ret


    import cv2
    class CameraHandler(HandleBase):
        def start(self):
            self.webcam = cv2.VideoCapture(0)
            self.frame_size = (
                self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
            )
            self.is_running = True

        def read(self):
            self.require_running()
            # We get a new frame from the webcam
            _, frame = self.webcam.read()
            if type(frame).__module__ == numpy.__name__:
                return frame
            else:
                return None

        def stop(self):
            self.require_running()
            self.webcam.release()
            cv2.destroyAllWindows()
            self.is_running = False


class RandomHandler(HandleBase):
    is_running = True

    def start(self):
        pass

    def stop(self):
        pass

    def read(self):
        return random.randint(-5, 5)


class FileHandler(HandleBase):
    def __init__(self, file):
        self.file = file
        self.file_conn = None

    def start(self):
        self.file_conn = open(self.file, "r")
        self.is_running = True

    def stop(self):
        self.require_running()
        self.file_conn.close()
        self.is_running = False

    def read(self):
        return self.file_conn.readline().rstrip()


class NullHandler(HandleBase):
    is_running = True

    def start(self):
        pass

    def stop(self):
        pass

    def read(self):
        return None

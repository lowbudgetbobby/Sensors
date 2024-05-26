import platform
from sensors.readerwriterbase import HandleBase

is_raspberrypi = False
try:
    if platform.uname().node == 'raspberrypi':
        import RPi.GPIO as GPIO
        import smbus
        is_raspberrypi = True
except Exception:
    pass


if not is_raspberrypi:
    import cv2

    class ImageToDesktopHandler(HandleBase):
        is_running = True

        def start(self):
            pass

        def stop(self):
            pass

        @staticmethod
        def resize(img, size):
            img = cv2.resize(img, size)
            return img

        def write(self, img, windowName):
            cv2.imshow(windowName, img)
            k = cv2.waitKey(1)
            if k == 27:
                cv2.destroyAllWindows()
                raise Exception('Key interupt. Stopping stream.')

            return True


    class StartStopButtonHandler(HandleBase):
        def write(self):
            pass

else:
    class ImageToDesktopHandler(HandleBase):
        is_running = True

        def start(self):
            raise Exception('Class not available on Raspberry PI')

        @staticmethod
        def resize(img, size):
            pass

        def write(self, img, windowName):
            pass


    READ_STATE_PIN = 5
    # WRITE_START_PIN = 6
    WRITE_RESET_PIN = 13

    class StartStopButtonHandler(HandleBase):
        def start(self):
            self._init_mem()
            self.write()
            self.is_running = True

        def _init_mem(self):
            GPIO.setup(READ_STATE_PIN, GPIO.IN)
            GPIO.setup(WRITE_RESET_PIN, GPIO.OUT)

        def write(self, *args, **kwargs):
            GPIO.output(WRITE_RESET_PIN, GPIO.HIGH)
            GPIO.output(WRITE_RESET_PIN, GPIO.LOW)

        def stop(self):
            self.require_running()
            GPIO.cleanup()
            self.is_running = False

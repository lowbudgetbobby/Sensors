import platform
from sensors.readerwriterbase import HandleBase, StateButtonHandlerBase

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


    class StateButtonHandler(StateButtonHandlerBase):
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

    class StateButtonHandler(StateButtonHandlerBase):
        def write(self, *args, **kwargs):
            self.reset()

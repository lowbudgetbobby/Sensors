import platform

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

    class ImageToDesktopHandler:

        @staticmethod
        def resize(img, size):
            img = cv2.resize(img, size)
            return img

        def write(self, img, windowName):
            cv2.imshow(windowName, img)
            k = cv2.waitKey(1)
            if k == 27:
                cv2.destroyAllWindows()
                return False

            return True

else:
    class ImageToDesktopHandler:
        @staticmethod
        def resize(img, size):
            pass

        def write(self, img, windowName):
            pass

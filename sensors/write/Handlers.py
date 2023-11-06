import cv2
import platform

is_raspberrypi = False
try:
    if platform.uname().node == 'raspberrypi':
        import RPi.GPIO as GPIO
        import smbus
        is_raspberrypi = True
except Exception:
    pass


class ImageToDesktopHandler:
    def write(self, img, windowName):
        cv2.imshow(windowName, img)
        k = cv2.waitKey(1)
        if k == 27:
            cv2.destroyAllWindows()
            return False

        return True

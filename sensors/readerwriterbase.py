import platform

is_raspberrypi = False
try:
    if platform.uname().node == 'raspberrypi':
        import RPi.GPIO as GPIO
        import smbus
        is_raspberrypi = True
except Exception:
    pass

class HandleBase:
    is_running = False
    def start(self):
        raise Exception('%s.%s: Method not implemented.' % (self.__class__, 'start'))

    def stop(self):
        raise Exception('%s.%s: Method not implemented.' % (self.__class__, 'stop'))

    def read(self):
        raise Exception('%s.%s: Method not implemented.' % (self.__class__, 'read'))

    def write(self, *args, **kwargs):
        raise Exception('%s.%s: Method not implemented.' % (self.__class__, 'write'))

    def require_running(self):
        if not self.is_running:
            raise Exception('%s: Connection not running.' % self.__class__)


if is_raspberrypi:
    READ_STATE_PIN = 5
    # WRITE_START_PIN = 6
    WRITE_RESET_PIN = 13

    class StateButtonHandlerBase(HandleBase):
        def start(self):
            self._init_mem()
            self.reset()
            self.is_running = True

        def _init_mem(self):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(READ_STATE_PIN, GPIO.IN)
            GPIO.setup(WRITE_RESET_PIN, GPIO.OUT)

        def reset(self):
            GPIO.output(WRITE_RESET_PIN, GPIO.HIGH)
            GPIO.output(WRITE_RESET_PIN, GPIO.LOW)

        def stop(self):
            self.require_running()
            GPIO.cleanup()
            self.is_running = False
else:
    class StateButtonHandlerBase(HandleBase):
        pass



class ReaderWriter:
    handle = None
    data = None
    error = None

    def __init__(self, handle: HandleBase):
        self.handle = handle

    def do_readwrite(self, *args, **kwargs):
        try:
            if not self.handle.is_running:
                self.handle.start()

            self.data = self.do(*args, **kwargs)
        except Exception as e:
            self.error = e
            self.handle.stop()

    def do(self, *args, **kwargs):
        # read/write specific code goes here.
        raise Exception('%s.%s: Method not implemented' % (self.__class__, 'do'))

    def close(self):
        if self.handle and self.handle.is_running:
            self.handle.stop()


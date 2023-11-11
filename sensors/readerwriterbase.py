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


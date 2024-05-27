from multiprocessing import Queue, Event
import multiprocessing as mp
from sensors.readerwriterbase import ReaderWriter

if __name__ == '__main__' and mp.get_start_method() != 'spawn':
    mp.set_start_method('spawn')


class ManageReaderWriter:
    def __init__(self, reader_writer: ReaderWriter):
        self.proc = None
        self.queue = None
        self.error_queue = None
        self.thread = None
        self.clear_event = None
        self.exit = None

        self.is_running = False
        # @todo make this into a list of readers so I can have 1 manager
        # pool multiple processes at once and manage.
        self.reader_writer = reader_writer

    def _do_thread_proc(self, queue, error_queue, clear_event, exit):
        while not exit.is_set():
            self._thread_loop(queue, error_queue, clear_event)

        self.is_running = False

    def _thread_loop(self, queue, error_queue, clear_event):
        raise Exception('method not implemented')

    def runProc(self):
        self.queue = Queue(maxsize=1)
        self.error_queue = Queue(maxsize=1)
        self.clear_event = Event()
        self.exit = Event()
        self.thread = mp.Process(target=self._do_thread_proc, args=(self.queue, self.error_queue, self.clear_event, self.exit))
        self.thread.daemon = True  # thread dies with the program
        self.thread.start()
        self.is_running = True

    def stopProc(self):
        self.exit.set()

import os
from multiprocessing import Queue, Event
import multiprocessing as mp

if __name__ == '__main__' and mp.get_start_method() != 'spawn':
    mp.set_start_method('spawn')


class ManageWriter:
    def __init__(self, writer):
        self.proc = None
        self.queue = None
        self.thread = None
        self.clear_event = None
        # @todo make this into a list of readers so I can have 1 manager
        # pool multiple processes at once and manage.
        self.writer = writer

    def _do_thread_proc(self, queue, clear_event):
        while True:
            if not queue.empty():
                data = self.queue.get()
                success = self.writer.do_write(data)
                if not success:
                    clear_event.set()

    def runProc(self):
        self.queue = Queue(maxsize=1)
        self.clear_event = Event()
        self.thread = mp.Process(target=self._do_thread_proc, args=(self.queue, self.clear_event))
        self.thread.daemon = True  # thread dies with the program
        self.thread.start()

    def writeProc(self, data):
        if self.queue.full():
            try:
                self.queue.get_nowait()
            except Exception:
                pass

        self.queue.put(data)
        if self.clear_event.is_set():
            raise Exception('Subprocess failed')

import os
from multiprocessing import Queue, Event
import multiprocessing as mp
from sensors.read.Readers import Reader


directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)
if __name__ == '__main__' and mp.get_start_method() != 'spawn':
    mp.set_start_method('spawn')


class ManageRead:
    def __init__(self, reader: Reader):
        self.proc = None
        self.queue = None
        self.error_queue = None
        self.thread = None
        self.clear_event = None
        # @todo make this into a list of readers so I can have 1 manager
        # pool multiple processes at once and manage.
        self.reader = reader

    def _do_thread_proc(self, queue, error_queue, clear_event):
        while True:
            while not queue.empty():
                # remove whatever is queued so we can refresh the value.
                try:
                    queue.get_nowait()
                except Exception:
                    pass

            if clear_event.is_set():
                self.reader.dump()
                clear_event.clear()

            data, error = self.reader.do_read()
            if error:
                error_queue.put(error)
            else:
                queue.put(data)

    def runProc(self):
        self.queue = Queue(maxsize=1)
        self.error_queue = Queue(maxsize=1)
        self.clear_event = Event()
        self.thread = mp.Process(target=self._do_thread_proc, args=(self.queue, self.error_queue, self.clear_event))
        self.thread.daemon = True  # thread dies with the program
        self.thread.start()

    def readProc(self, reset_data=True):
        error = None
        try:
            error = self.error_queue.get_nowait()
        except Exception:
            pass
        if error:
            raise Exception(error)

        try:
            val = self.queue.get()
        except Exception:
            val = None

        if reset_data:
            self.clear_event.set()
        return val

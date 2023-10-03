import os
from multiprocessing import Queue, Event
import multiprocessing as mp


directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)
if mp.get_start_method() != 'spawn':
    mp.set_start_method('spawn')


class ManageRead:
    def __init__(self, reader):
        self.proc = None
        self.queue = None
        self.thread = None
        self.clear_event = None
        # @todo make this into a list of readers so I can have 1 manager
        # pool multiple processes at once and manage.
        self.reader = reader

    def _do_thread_proc(self, queue, clear_event):
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

            self.reader.do_read()
            queue.put(self.reader.data)

    def runProc(self):
        self.queue = Queue(maxsize=1)
        self.clear_event = Event()
        self.thread = mp.Process(target=self._do_thread_proc, args=(self.queue, self.clear_event))
        self.thread.daemon = True  # thread dies with the program
        self.thread.start()

    def readProc(self, wait=True, reset_data=True):
        try:
            val = self.queue.get()
        except Exception:
            val = None

        if reset_data:
            self.clear_event.set()
        return val

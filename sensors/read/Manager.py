import os
from multiprocessing import Queue
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
        # @todo make this into a list of readers so I can have 1 manager
        # pool multiple processes at once and manage.
        self.reader = reader

    def _do_thread_proc(self, queue):
        for val in self.reader.read():
            if not queue.empty():
                queue.get()  # remove whatever is queued so we can refresh the value.
            queue.put(val)

    def runProc(self):
        self.queue = Queue(maxsize=1)
        self.thread = mp.Process(target=self._do_thread_proc, args=(self.queue,))
        self.thread.daemon = True  # thread dies with the program
        self.thread.start()

    def readProc(self, wait=True, reset_data=True):
        # I'm not fully sure why the following works...but it does...I presume because this technically
        # forces a wait on when the queue has a value...I'm going to ignore this for now and just leave it.
        val = self.queue.get()
        while True:
            try:
                line = self.queue.get()
            except Exception:
                line = None
            if line is not None:
                val = line
                break
            if not wait:
                break
        if reset_data:
            open(f"{parent_dir}/flag_files/.clear-{self.reader.name}", "w")
        return val

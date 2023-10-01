import subprocess
import os
import time
# from queue import Queue, Empty
from multiprocessing import Queue
from threading import Thread
import multiprocessing as mp
import json

directory = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(directory)


class ManageRead:
    def __init__(self, reader):
        self.proc = None
        self.queue = None
        self.thread = None
        self.reader = reader

    def _do_thread_proc(self, queue):
        for val in self.reader.read():
            if not queue.empty():
                queue.get() # remove whatever is queued.
            queue.put(val)

    def runProc(self):
        mp.set_start_method('spawn')
        self.queue = Queue(maxsize=1)
        self.thread = mp.Process(target=self._do_thread_proc, args=(self.queue,))
        self.thread.daemon = True  # thread dies with the program
        self.thread.start()
        # self.thread.join()

    def readProc(self, wait=True, reset_data=True):
        val = None
        while True:
            try:
                line = self.queue.get_nowait()
            except Exception:
                line = None
            if line:
                val = line
                break
            if not wait:
                break
        if reset_data:
            open(f"{parent_dir}/flag_files/.clear", "w")
        return json.loads(val)

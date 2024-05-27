import multiprocessing as mp
from sensors.read.Readers import Reader
from sensors import ManageReaderWriter

if __name__ == '__main__' and mp.get_start_method() != 'spawn':
    mp.set_start_method('spawn')


class ManageRead(ManageReaderWriter):
    def __init__(self, reader: Reader):
        super().__init__(reader)

    def _thread_loop(self, queue, error_queue, clear_event):
        while not queue.empty():
            # remove whatever is queued so we can refresh the value.
            try:
                queue.get_nowait()
            except Exception:
                pass

        if clear_event.is_set():
            self.reader_writer.dump()
            clear_event.clear()

        data, error = self.reader_writer.do_read()
        if error:
            error_queue.put(error)
        else:
            queue.put(data)

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

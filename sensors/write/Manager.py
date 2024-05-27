import multiprocessing as mp
from sensors.write.Writers import Writer
from sensors import ManageReaderWriter

if __name__ == '__main__' and mp.get_start_method() != 'spawn':
    mp.set_start_method('spawn')


class ManageWriter(ManageReaderWriter):
    def __init__(self, writer: Writer):
        super().__init__(writer)

    def _thread_loop(self, queue, error_queue, clear_event):
        if not queue.empty():
            data = self.queue.get()
            success, error = self.reader_writer.do_write(data)
            if not success:
                clear_event.set()
                error_queue.put(error)

    def writeProc(self, data):
        if self.queue.full():
            try:
                self.queue.get_nowait()
            except Exception:
                pass

        self.queue.put(data)
        if self.clear_event.is_set():
            prev_error = None
            try:
                prev_error = self.error_queue.get_nowait()
            except Exception:
                pass
            if prev_error:
                raise Exception(prev_error)

            raise Exception('Subprocess failed')

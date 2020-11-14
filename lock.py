import threading
from queue import Queue

class RWLock:
    def __init__(self):
        self.rwlock = 0
        """ if rwlock > 0, it records the number of reader
        if rwlock < 0, it records the number of writer(at most -1) """
        self.waiting_writers_queue = Queue()
        self.waiting_writers = 0 # the number of waiting writers
        self.lock = threading.RLock()
        self.readers_ok = threading.Condition(self.lock)

    def acquire_read(self):
        # Acquire for a read lock and exclusive with write lock
        self.lock.acquire()
        while self.rwlock < 0:
            self.readers_ok.wait()
        self.rwlock += 1
        self.lock.release()

    def acquire_write(self):
        # Acquire for a write lock and exclusive with read lock
        self.lock.acquire()
        while self.rwlock != 0:
            self.waiting_writers += 1
            writers_ok = threading.Condition(self.lock)
            self.waiting_writers_queue.put(writers_ok)
            writers_ok.wait()
            self.waiting_writers -= 1
        self.rwlock = -1
        self.lock.release()

    def release(self):
        # release a lock and inform others who are waiting
        self.lock.acquire()
        if self.rwlock < 0:
            self.rwlock = 0
        else:
            self.rwlock -= 1
        # inform waiting writers and readers
        wake_writers = self.waiting_writers and self.rwlock == 0
        wake_readers = self.waiting_writers == 0
        self.lock.release()
        if wake_writers:
            writers_ok = self.waiting_writers_queue.get_nowait()
            writers_ok.acquire()
            writers_ok.notify()
            writers_ok.release()
        elif wake_readers:
            self.readers_ok.acquire()
            self.readers_ok.notifyAll()
            self.readers_ok.release()

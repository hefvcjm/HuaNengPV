# coding = utf-8
import inspect
import ctypes
import threading
from typing import List
import sched
import time
import queue
from lib.logger import log


class Timer(threading.Thread):
    """Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=None, kwargs=None)
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval=None, function=None, args=None, kwargs=None):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.released = False
        self.finished = threading.Event()
        self.start()

    def new_timer(self, interval, function, args=None, kwargs=None):
        self.cancel()
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.released = False
        self.finished = threading.Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet."""
        self.finished.set()

    def release(self):
        self.cancel()
        self.released = True

    def run(self):
        while not self.released:
            if self.interval is not None and self.function is not None:
                self.finished.wait(self.interval)
                if not self.finished.is_set():
                    self.function(*self.args, **self.kwargs)
                self.finished.set()


def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class Thread(threading.Thread):
    '''A thread class that supports raising exception in the thread from
       another thread.
    '''
    timer = None

    def set_timer(self):
        if self.timer is None:
            self.timer = Timer()

    def get_my_tid(self):
        """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do : self.ident

        raise AssertionError("could not determine the thread's id")

    def raiseExc(self, exctype):
        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        self.timer.release()
        _async_raise(self.get_my_tid(), exctype)


_schedule = None
_lock = threading.Lock()


class ThreadPool:
    class _Task:
        def __init__(self, fn, callback, timeout, *args, **kwargs):
            self.fn = fn
            self.callback = callback
            self.timeout = timeout
            self.args = args
            self.kwargs = kwargs

        def run(self, thread: Thread):
            thread.set_timer()
            thread.timer.new_timer(self.timeout, thread.raiseExc, [Exception])
            # print("call: ", self.fn.__name__)
            result = self.fn(*self.args, **self.kwargs)
            # print(result)
            thread.timer.cancel()
            if self.callback is not None:
                self.callback(result)
            return result

    def _worker(self, thread, task_queue: queue.Queue):
        while True:
            task = task_queue.get(block=True)
            log.info(f"task queue remain: {task_queue.qsize()}")
            if task is not None:
                task.run(thread[0])

    def __init__(self, max_pool, queue_size=None):
        global _schedule
        self.__thread_num = max_pool
        self.__queue_size = queue_size
        self.__task_queue = queue.Queue(maxsize=self.__queue_size)
        self.__threads = set()
        _schedule = sched.scheduler(time.time, time.sleep)
        # self.__schedule.enter(1, 0, self._interval_check)
        self._interval_check()
        t = threading.Thread(target=_schedule.run)
        t.start()

    def submit(self, fn, callback, timeout, *args, **kwargs):
        with _lock:
            self.__task_queue.put(self._Task(fn, callback, timeout, *args, **kwargs))
            log.info(f"task queue: {self.__task_queue.qsize()}")
            self._adjust_thread_count()

    def _adjust_thread_count(self):
        self._check_thread()
        num_threads = len(self.__threads)
        if num_threads < self.__thread_num:
            temp = []
            t = Thread(target=self._worker, args=(temp, self.__task_queue))
            temp.append(t)
            t.daemon = True
            t.start()
            self.__threads.add(t)

    def _interval_check(self):
        _schedule.enter(1, 0, self._interval_check)
        self._adjust_thread_count()

    def _check_thread(self):
        # print("_check_thread")
        self.__threads = set(filter(lambda x: x.is_alive(), self.__threads))
        # print(f"after check: {len(self.__threads)}")

# s = sched.scheduler(time.time, time.sleep)
#
#
# def _interval_check():
#     s.enter(1, 0, _interval_check)
#     print("test")
#
#
# s.enter(1, 0, _interval_check)
# threading.Thread(target=s.run).start()
# if __name__ == '__main__':
#
#     import time
#
#
#     def loop(i=0):
#         try:
#             while True:
#                 print(f"loop_{i}")
#                 time.sleep(1)
#         except Exception as e:
#             print(e)
#
#
#     thread_pool = ThreadPool(5, 1000)
#     i = 0
#     while True:
#         i += 1
#         thread_pool.submit(loop, None, 10, i)
#         time.sleep(1)

# thread = Thread(target=loop)
# thread.start()
# thread.set_timer()
# thread.timer.new_timer(5, thread.raiseExc, [Exception])

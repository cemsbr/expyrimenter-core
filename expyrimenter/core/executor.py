from concurrent.futures import ThreadPoolExecutor
from .config import Config
from collections import deque, namedtuple
from threading import Lock, RLock


class Wait:
    pass


FutureParams = namedtuple('FutureParams', ['fn', 'args', 'kwargs'])


class Executor:
    def __init__(self, max_workers=None):
        if max_workers is None:
            max_workers = int(Config('executor').get('max_concurrency'))

        self._executor = ThreadPoolExecutor(max_workers)
        self._futures = []
        self._queue = deque()
        self._working_lock = Lock()
        self._tasks_lock = RLock()

    def run(self, runnable, *args, **kwargs):
        """Submits Runnable objects to be scheduled.

        They can be submitted right away or after a barrier added by
        add_barrier().
        """
        with self._tasks_lock:
            submit_fn = self._enqueue if self._queue else self._run_now
            return submit_fn(runnable.run, *args, **kwargs)

    def _run_now(self, fn, *args, **kwargs):
        """Must be thread-safe, called by _dequeue_once()"""
        if not self._futures and not self._queue:
            self._working_lock.acquire()

        future = self._executor.submit(fn, *args, **kwargs)
        future.add_done_callback(self._callback)
        self._futures.append(future)
        return future

    def add_barrier(self):
        """Non-blocking. Wait tasks to finish before running new ones.

        After calling this method, next submitted tasks will be run after all
        previous tasks are done. The blocking version of this method is wait().
        """
        with self._tasks_lock:
            if self._queue or self._futures:
                self._queue.append(Wait())

    def wait(self):
        """Blocks untill all tasks are done. You must call it (or shutdown()) at
        least in the end. See also add_barrier().
        """
        self._working_lock.acquire()
        self._working_lock.release()

    def shutdown(self):
        """Waits tasks, frees resources and makes this instance unusable.

        Don't use this object after calling this method.
        """
        self.wait()
        self._executor.shutdown()

    def _enqueue(self, fn, *args, **kwargs):
        future_params = FutureParams(fn, args, kwargs)
        self._queue.append(future_params)

    def _callback(self, future):
        """Must be thread-safe because of python specs."""
        with self._tasks_lock:
            self._futures.remove(future)
            if not self._futures:
                if self._queue:
                    self._dequeue_once()
                else:
                    self._working_lock.release()

    def _dequeue_once(self):
        # If the user adds two or more barriers, we don't get stuck
        while self._queue and isinstance(self._queue[0], Wait):
            self._queue.popleft()
        if not self._queue:
            self._working_lock.release()
        while self._queue and isinstance(self._queue[0], FutureParams):
            task = self._queue[0]
            self._run_now(task.fn, *task.args, **task.kwargs)
            self._queue.popleft()

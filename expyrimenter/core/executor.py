from concurrent.futures import ThreadPoolExecutor
from . import Config
import concurrent.futures
from collections import deque, namedtuple


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

    def run(self, runnable, *args, **kwargs):
        """Submits Runnable objects to be scheduled.

        They can be submitted right away or after a barrier added by
        add_barrier().
        """
        run_fn = self._enqueue if self._queue else self._run_now
        return run_fn(runnable.run, *args, **kwargs)

    def add_barrier(self):
        """Non-blocking. Wait tasks to finish before running new ones.

        After calling this method, next submitted tasks will be run after all
        previous tasks are done. The blocking version of this method is wait().
        """
        self._queue.append(Wait())

    def wait(self):
        """Blocks untill all tasks are done. You must call it (or shutdown()) at
        least in the end. See also add_barrier().
        """
        self._wait_futures()
        while self._queue:
            self._dequeue_once()
            self._wait_futures()

    def shutdown(self):
        """Waits tasks, frees resources and makes this instance unusable.

        Don't use this object after calling this method.
        """
        self.wait()
        self._executor.shutdown()

    def _enqueue(self, runnable, *args, **kwargs):
        future_params = FutureParams(runnable, args, kwargs)
        self._queue.append(future_params)

    def _run_now(self, runnable, *args, **kwargs):
        """Must be thread-safe, called by _dequeue_once()"""

        future = self._executor.submit(runnable, *args, **kwargs)
        self._futures.append(future)
        future.add_done_callback(self._callback)
        return future

    def _wait_futures(self):
        if self._futures:
            concurrent.futures.wait(self._futures)
        if self._queue and isinstance(self._queue[0], Wait):
            self._queue.popleft()

    def _dequeue_once(self):
        """Must be thread-safe, called by _callback."""
        while self._queue and isinstance(self._queue[0], FutureParams):
            # Make sure a task is either in self._queue or in self._futures,
            # so we can check for pending tasks safely.
            task = self._queue[0]
            self._run_now(task.fn, *task.args, **task.kwargs)
            self._queue.popleft()

    def _callback(self, future):
        """Must be thread-safe because of python specs."""
        self._futures.remove(future)
        if not self._futures and self._queue:
            self._dequeue_once()

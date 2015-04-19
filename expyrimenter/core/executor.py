from concurrent.futures import ThreadPoolExecutor
from . import Config
import concurrent.futures


class Executor:
    def __init__(s, max_workers=None):
        if max_workers is None:
            max_workers = int(Config('executor').get('max_concurrency'))

        s._executor = ThreadPoolExecutor(max_workers)
        s._futures = []

    def run(s, runnable, *args, **kwargs):
        """Submits Runnable objects to the PoolExector.

        Using Runnable objects, you have more control and verbosity.
        Useful when things go wrong (we know it always happens).
        """
        future = s._executor.submit(runnable.run, *args, **kwargs)
        s._futures.append(future)
        future.add_done_callback(s._futures.remove)
        return future

    def wait(s):
        current_futures = list(s._futures)
        concurrent.futures.wait(current_futures)

    def shutdown(s):
        """Waits tasks, frees resources and makes this instance unusable.

        Don't use this object after calling this method.
        """
        s._executor.shutdown()

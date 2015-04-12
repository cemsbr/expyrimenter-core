from .runnable import Runnable
import logging
from urllib.error import HTTPError


class Function(Runnable):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def run(self):
        logger = logging.getLogger('function')
        try:
            self.output = self._function(*self._args, **self._kwargs)
            self.failed = False
            return self.output
            msgs = None
        except Exception as e:
            self.failed = True
            msgs = ['{} - {}'.format(type(e).__name__, str(e))]
            if type(e) is HTTPError:
                msgs.append('"{}"'.format(e.read()))
        finally:
            self.executed = True
            self.log(logger, msgs)

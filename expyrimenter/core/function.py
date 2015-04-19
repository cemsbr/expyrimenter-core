from .runnable import Runnable


class Function(Runnable):
    def __init__(self, fn, title=None, logger_name=None):
        if title is None:
            title = ' '.join((type(self).__name__, fn.__name__, id(self)))
        if logger_name is None:
            logger_name = 'function'
        super().__init__(title=title, logger_name=logger_name)

        self._fn = fn
        self._args = ()
        self._kwargs = {}

    def set_args(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def run(self):
        self.run_pre()

        try:
            output = self._fn(*self._args, **self._kwargs)
            self._logger.success(self.title)
        except Exception as e:
            self._logger.failure(self.title, e)
            raise e
        finally:
            self.run_pos()

        return output

from .expylogger import ExpyLogger


class Runnable:
    def __init__(self, log_name=None, title=None):
        if title is None:
            title = self._id()
        self.title = title
        self._logger = ExpyLogger(title, log_name)

    def run(self):
        raise NotImplementedError('Runnable.run not implemented')

    def _id(self):
        return '{} {:d}'.format(type(self).__name__, id(self))

    def run_pre(self):
        self._logger.start()

    def run_pos(self):
        self._logger.end()

    def __str__(self):
        return 'runnable "{}"'.format(self.title)

import logging
from logging import Logger
from subprocess import CalledProcessError


class ExpyLogger:
    """Standardizes log messages and simplifies :py:module:`logging`."""

    #: Default logger name for new instances
    name = 'expyrimenter'

    configured = False

    def __init__(self, title, name=None):
        self.title = title
        log_name = name if name else Logger.name
        self._logger = logging.getLogger(log_name)
        if not ExpyLogger.configured:
            ExpyLogger.config()

    @classmethod
    def config(cls, level=None, format=None):
        if level is None:
            level = logging.INFO
        if format is None:
            format = '%(asctime)s|%(levelname)s|%(name)s|%(message)s'

        logging.basicConfig(level=level, format=format)
        cls.configured = True

    def start(self, level=logging.DEBUG):
        self._logger.log(level, 'starting "%s"', self.title)

    def end(self, level=logging.DEBUG):
        self._logger.log(level, 'finished "%s"', self.title)

    def success(self, level=logging.INFO):
        self._logger.log(level, 'success  "%s"', self.title)

    def failure(self, exception=None, level=logging.ERROR):
        msg, args = 'failure  "%s"', [self.title]
        if exception:
            msg, args = self._add_exception_info(exception, msg, args)
        self._logger.log(level, msg, *args)

    def _add_exception_info(self, exception, msg, args):
        if isinstance(exception, CalledProcessError):
            msg += ', return code %d'
            args.append(exception.returncode)
            if exception.output:
                msg += ', output "%s"'
                args.append(exception.output.rstrip())
        else:
            msg += ', %s'
            args.append(exception)
        return msg, args

    # Methods from standard Logger
    @classmethod
    def set_debug(cls):
        cls.config(logging.DEBUG)

    @classmethod
    def set_info(cls):
        cls.config(logging.INFO)

    @classmethod
    def set_warning(cls):
        cls.config(logging.WARNING)

    @classmethod
    def set_error(cls):
        cls.config(logging.ERROR)

    @classmethod
    def set_critical(cls):
        cls.config(logging.CRITICAl)

    # Methods from Logger

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._logger.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self._logger.log(level, msg, *args, **kwargs)

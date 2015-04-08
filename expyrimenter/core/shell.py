import logging
import subprocess
from subprocess import CalledProcessError
from .runnable import Runnable


class Shell(Runnable):
    """
    :param str cmd: Command with arguments to be run.
    :param str title: A title to be displayed in log outputs.
                      If None, :attr:`cmd` will be shown.
    :param bool stdout: Whether or not to display standard output.
                        Default is *False*.
    :param bool stderr: Whether or not to display standard error.
                        Default is *True*.
    """

    def __init__(self, cmd, title=None, stdout=False, stderr=True):
        super().__init__()
        self._cmd = self._redirect_outputs(cmd, stdout, stderr)
        self._title, self._stdout, self._stderr = title, stdout, stderr
        self._log = logging.getLogger('shell')

    def _redirect_outputs(self, cmd, stdout, stderr):
        """
        Avoid transfering unnecessary output through the network.
        If local, keeps the output clean.
        """
        suffix = ''
        if not stdout:
            suffix += ' 1>/dev/null'
        if not stderr:
            suffix += ' 2>/dev/null'

        return cmd + suffix

    def _title_cmd(self):
        return self._title if self._title else self._cmd

    def run_pre(self):
        self._log.debug('beginning:' + self._title_cmd())

    def run(self):
        """If the command exits 0, returns 0 or selected (stdout/stderr) output.
        Otherwise, logs the error and raises CalledProcessError.

        :return: shell return code (0) or selected output.
        :rtype: int or str
        :raises CalledProcessError: if shell return code is not 0.
        """
        self.run_pre()

        kwargs = {'shell': True, 'universal_newlines': True}
        if self._stderr:
            kwargs['stderr'] = subprocess.STDOUT

        if not (self._stdout or self._stderr):
            self.output = subprocess.check_call(self._cmd, **kwargs)
            self.run_pos()
        else:
            try:
                self.output = subprocess.check_output(self._cmd,
                                                      **kwargs).strip()
                self._log.info('success ' + self._title_cmd())
                self.failed = False
            except CalledProcessError as e:
                self.output = 'failure {} - code {}'.format(self._title_cmd(),
                                                            e.returncode)
                if e.output:
                    self.output += ', output "{}"'.format(e.output.rstrip())
                self._log.error(self.output)
                self.failed = True
                raise e
            finally:
                self.executed = True
                self.run_pos()

        return self.output

    def was_successful(self):
        """Runs the command and returns whether the return code is 0.

        :return: whether the command was successful.
        :rtype: bool
        """
        try:
            self.run()
            return True
        except CalledProcessError:
            return False

    def has_failed(self):
        """Runs the command and returns whether the return code differs from 0.

        :return: whether the command has failed.
        :rtype: bool
        """
        return not self.was_successful()

    def run_pos(self):
        self._log.debug('finished:' + self._title_cmd())

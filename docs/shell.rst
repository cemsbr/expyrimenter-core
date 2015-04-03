Shell
=====

This is one of the innermost classes.
The parameters are passed to the constructor and then
you can call :func:`run() <expyrimenter.core.Shell.run>` or
use an :class:`Executor <expyrimenter.core.Executor>`
instance to run in parallel.

  >>> from expyrimenter.core import Shell
  >>> Shell('echo Hello', stdout=True).run()
  'Hello'
  >>> # You can also use try/except
  >>> from subprocess import CalledProcessError
  >>> try:
  >>>     Shell('wrongcommand').run()
  >>> except CalledProcessError as e:
  >>>     print("Failed: %s" % e.output)
  Failed: /bin/sh: 1: wrongcommand: not found

.. automodule:: expyrimenter.core

.. autoclass:: Shell
    :members:
    :show-inheritance:

Pushbullet
==========

Experiments may crash, so you probably watch their outputs every few minutes
to make sure it is still running or restart it in the worst case.
Now, there's no need to keep an eye on the output anymore!
By using this code, you will receive a message
in your mobile phone and desktop browser
if a log file is not updated often enough.
You can also send messages at any time, for example,
when the experiment finishes.

The code below sends a message if a file is not updated in 5 minutes.
The script will keep running until it sends a message or it is killed. ::

  from expyrimenter.apps import Pushbullet

  pb = Pushbullet()
  pb.monitor_file('~/outputs/long_experiment.log', 5 * 60)

To send a message::

  from expyrimenter.apps import Pushbullet

  pb = Pushbullet()
  # To send a message, inform title and an optional body
  pb.send_note('Experiment finished!')

Before using it, you must install pushbullet mobile app and/or browser add-on.
Then, go to the `Pushbullet web site <https://www.pushbullet.com>`_,
access your account settings (last time, it was by clicking in the avatar),
copy the Access Token and paste it in your ``~/.expyrimenter/config.ini``
like this
(check :class:`expyrimenter.Config` for more details about general
configuration):

.. code-block:: ini

  [pushbullet]
  token = your_pushbullet_access_token

.. automodule:: expyrimenter.apps

.. autoclass:: Pushbullet
    :members:

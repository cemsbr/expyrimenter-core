import unittest
from unittest.mock import Mock, patch
from expyrimenter.apps import Pushbullet
from expyrimenter import Config


@patch.object(Config, 'get')
class TestPushbullet(unittest.TestCase):

    @patch('expyrimenter.apps.pushbullet.logging')
    def test_no_key_in_config(self, logging, cfg):
        cfg.return_value = None
        self.assertRaises(AttributeError, Pushbullet)

    @patch('expyrimenter.apps.pushbullet.Pushbullet.send_note')
    @patch('expyrimenter.apps.pushbullet.time')
    @patch('expyrimenter.apps.pushbullet.getmtime')
    def test_one_note_when_file_is_not_modified(self, getmtime, time,
                                                note_method, cfg):
        getmtime.return_value = 3
        time.time.return_value = 20
        cfg.return_value = ''
        Pushbullet().monitor_file('/tmp/test', 10)
        self.assertEqual(1, note_method.call_count)

    @patch('expyrimenter.apps.pushbullet.Pushbullet.send_note')
    @patch('expyrimenter.apps.pushbullet.time')
    @patch('expyrimenter.apps.pushbullet.getmtime')
    def test_when_file_is_modified(self, getmtime, time, note_method, cfg):
        getmtime.return_value = 3
        time.time.return_value = 10
        time.sleep.side_effect = DontSleepException
        cfg.return_value = ''

        try:
            Pushbullet().monitor_file('/tmp/test', 10)
        except DontSleepException:
            pass

        self.assertEqual(0, note_method.call_count)

    @patch('expyrimenter.apps.pushbullet.Pushbullet.send_note')
    @patch('expyrimenter.apps.pushbullet.time')
    @patch('expyrimenter.apps.pushbullet.getmtime')
    def test_custom_note(self, getmtime, time, note_method, cfg):
        getmtime.return_value = 3
        time.time.return_value = 20
        cfg.return_value = ''

        title, body = 'Test title', 'Test body'
        Pushbullet().monitor_file('/tmp/file', 10, title, body)
        note_method.assert_called_once_with(title, body)

    @patch('expyrimenter.apps.pushbullet.requests.post')
    def test_note_post(self, post, cfg):
        post.return_value.status_code = 200
        cfg.return_value = ''

        pb = Pushbullet()
        pb.send_note('title', 'body')
        self.assertTrue(post.called)

    @patch('expyrimenter.apps.pushbullet.requests.post')
    def test_note_success(self, post, cfg):
        post.return_value.status_code = 200
        cfg.return_value = ''

        pb = Pushbullet()
        pb._log = Mock()
        pb.send_note('title', 'body')
        self.assertTrue(pb._log.info.called)

    @patch('expyrimenter.apps.pushbullet.requests.post')
    def test_note_failure(self, post, cfg):
        post.return_value.status_code = 404
        post.return_value.json.return_value = ''
        cfg.return_value = ''
        pb = Pushbullet()
        pb._log = Mock()

        pb.send_note('title', 'body')
        self.assertEqual(1, post.call_count)
        self.assertTrue(pb._log.error.called)


class DontSleepException(Exception):

    def __init__(self):
        super().__init__('Avoiding sleep in test code')

if __name__ == '__main__':
    unittest.main()

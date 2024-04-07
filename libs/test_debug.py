import os
import unittest
from unittest import mock
from unittest.mock import patch
from debug import *

class TestDebug(unittest.TestCase):

    @mock.patch.dict(os.environ, {"DEBUG": "on"})
    def test_debug_on(self):
        # then
        self.assertEqual(os.environ.get('DEBUG'), "on")

    @mock.patch.dict(os.environ, {"DEBUG": "off"})
    def test_debug_off(self):
        # then
        self.assertEqual(os.environ.get('DEBUG'), "off")

    @patch('debug.time.time')
    @patch('debug.memory_usage')
    def test_start_with_debug_on(self, mock_memory_usage, mock_time):
        with patch.dict(os.environ, {"DEBUG": "on"}):
            # when
            mock_time.return_value = 1234.5
            mock_memory_usage.return_value = [100]

            Debug.start()

            # then
            self.assertEqual(Debug.start_time, 1234.5)
            self.assertEqual(Debug.mem_usage_start, 100) 

    @patch('debug.time.time')
    @patch('debug.memory_usage')
    @patch('sys.stdout', new=unittest.mock.MagicMock())
    def test_end_with_debug_on(self, mock_memory_usage, mock_time, mock_stdout):
        with patch.dict('os.environ', {"DEBUG": "on"}):
            # when
            mock_time.return_value = 1236.5
            Debug.start_time = 1234.5
            Debug.mem_usage_start = 50
            mock_memory_usage.return_value = [150]

            Debug.end()

            # then
            mock_time.assert_called()
            mock_memory_usage.assert_called()
            output = mock_stdout.write.call_args[0][0]

            self.assertIn("Execution time: 2.0 seconds", output)
            self.assertIn("Memory usage: 100 MiB", output)

    @patch("builtins.open", unittest.mock.mock_open())
    def test_infoDict(self, mocked_file):
        with patch.dict('os.environ', {"DEBUG": "on"}):
            # when
            Debug.infoDict(mocked_file, {"test_word" : ["test_token"]})

            # then
            mocked_file.assert_called_once()
            mocked_file().write.assert_called_once_with("word: test_word tokens: ['test_token'] \n")

    @patch("builtins.open", unittest.mock.mock_open())
    def test_infoList(self, mocked_file):
        with patch.dict('os.environ', {"DEBUG": "on"}):
            # when
            Debug.infoList(mocked_file, [("str1", "str2", "str3")])

            # then
            mocked_file.assert_called_once()
            mocked_file().write.assert_called_once_with("str1: str1, str2: str2 str3: str3 \n")         
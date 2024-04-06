import unittest
from unittest.mock import mock_open, patch
from handler import FileHandler, CounterProcessor  # your_module을 해당 모듈명으로 변경

class TestFileHandler(unittest.TestCase):
    def test_read(self):
        expected_content = "test content"
        with patch("builtins.open", mock_open(read_data=expected_content), create=True) as mocked_file:
            result = FileHandler.read("dummy.txt")
            mocked_file.assert_called_once_with("dummy.txt", "r", encoding="utf-8")
            self.assertEqual(result, expected_content)

    def test_save(self):
        test_data = [("school1", 10), ("school2", 20)]
        with patch("builtins.open", mock_open(), create=True) as mocked_file:
            with patch("os.path.exists", return_value=False):
                with patch("os.makedirs") as mocked_makedirs:
                    result_filename = FileHandler.save(test_data)
                    mocked_makedirs.assert_called_once()
                    mocked_file().write.assert_any_call("school1\t10\n")
                    mocked_file().write.assert_any_call("school2\t20\n")
                    self.assertIn("result.", result_filename)

class TestCounterProcessor(unittest.TestCase):
    def test_count(self):
        test_word = ['school', 'school', 'school', 'test', 'test']
        expected_result = [('school', 3), ('test', 2)]
        result = CounterProcessor.count(test_word)
        self.assertEqual(result, expected_result)

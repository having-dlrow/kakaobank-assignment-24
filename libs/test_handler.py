import unittest
from unittest.mock import mock_open, patch
from handler import FileHandler, CounterHandler


class TestFileHandler(unittest.TestCase):

  def setUp(self):
    self.handler = FileHandler()
    self.TEST_DIR = "dir"
    self.TEST_FILENAME = "dummy.txt"
    self.TEST_CONTENT = "test content"
    self.TEST_DATA = [("data1", 10), ("data2", 20)]

  def test_read(self):
    """파일 읽기"""
    with patch('builtins.open',
               mock_open(read_data="test content"),
               create=True) as mocked_open:
      # when
      result = FileHandler().read(self.TEST_FILENAME)

      # then
      mocked_open.assert_called_once_with(self.TEST_FILENAME,
                                          "r",
                                          encoding="utf-8")
      self.assertEqual(result, self.TEST_CONTENT)

  def test_write(self):
    """파일 저장"""
    with patch('builtins.open', mock_open(), create=True) as mocked_open:
      # when
      self.handler.write(self.TEST_FILENAME, self.TEST_DATA)

      # then
      mocked_open.assert_called_once_with(self.TEST_FILENAME,
                                          'w',
                                          encoding='utf-8')
      mocked_open().write.assert_any_call("data1\t10\n")
      mocked_open().write.assert_any_call("data2\t20\n")

  def test_save(self):
    """파일 저장"""
    with patch.object(self.handler, '_FileHandler__is_dir', return_value=True), \
         patch.object(self.handler, '_FileHandler__add_datetime', return_value=self.TEST_FILENAME), \
         patch.object(self.handler, 'write') as mocked_write:
      # when
      filename = self.handler.save(self.TEST_DATA, self.TEST_DIR,
                                   self.TEST_FILENAME)
      # then
      self.assertEqual(filename, self.TEST_FILENAME)
      mocked_write.assert_called_once()

  def test_add_datetime(self):
    """@private test"""
    # when
    result = self.handler._FileHandler__add_datetime(self.TEST_FILENAME)

    # then
    self.assertTrue(result.startswith(self.TEST_FILENAME))
    self.assertTrue(result.endswith('.txt'))

  def test_is_dir(self):
    with patch('os.path.exists', return_value=False), \
         patch('os.makedirs') as mocked_makedirs:
      """@private test"""
      # when
      result = self.handler._FileHandler__is_dir(self.TEST_DIR)
      # then
      self.assertTrue(result)
      mocked_makedirs.assert_called_once_with(self.TEST_DIR)


class TestCounterHandler(unittest.TestCase):

  def setUp(self):
    self.handler = CounterHandler()
    self.TEST_COUNT_WORDS = ['school', 'school', 'school', 'test', 'test']

  def test_count(self):
    """List Count"""
    # when
    result = self.handler.count(self.TEST_COUNT_WORDS)

    # then
    self.assertEqual(result, [('school', 3), ('test', 2)])

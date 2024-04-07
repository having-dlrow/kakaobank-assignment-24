import os
import unittest
from unittest import mock
from unittest.mock import patch, mock_open, call
from debug import *


class TestDebug(unittest.TestCase):

  def setUp(self):
    self.TEST_DICT = {'key1': 'value1', 'key2': 'value2'}
    self.TEST_LIST = [('item1', 'item2'), ('item3', 'item4')]
    self.TEST_FILENAME = 'debug_file.txt'

  @mock.patch.dict(os.environ, {"DEBUG": "on"})
  def test_debug_on(self):
    """환경변수 테스트"""
    # then
    self.assertEqual(os.environ.get('DEBUG'), "on")

  @mock.patch.dict(os.environ, {"DEBUG": "off"})
  def test_debug_off(self):
    """환경변수 테스트"""
    # then
    self.assertEqual(os.environ.get('DEBUG'), "off")

  @patch('debug.Debug.on', True)
  @patch('debug.time.time')
  @patch('debug.memory_usage')
  def test_start_with_debug_on(self, mock_memory_usage, mock_time):
    """디버그 시작 테스트"""
    # Given
    mock_time.return_value = 1234.5
    mock_memory_usage.return_value = [100]

    # when
    Debug.start()

    # then
    self.assertEqual(Debug.start_time, 1234.5)
    self.assertEqual(Debug.mem_usage_start, 100)

  @patch('debug.Debug.on', True)
  @patch('debug.time.time')
  @patch('debug.memory_usage')
  @patch('builtins.print')
  def test_end_with_debug_on(self, mock_print, mock_memory_usage, mock_time):
    """디버그 끝 테스트"""
    # Given
    mock_time.side_effect = [1234.5, 1236.5]  # start와 end 시간
    mock_memory_usage.side_effect = [[50], [150]]  # start와 end 메모리 사용량

    # when
    Debug.start()
    Debug.end()

    # Then
    expected_execution_time = "Execution time: 2.0 seconds"
    expected_memory_usage = "Memory usage: 100 MiB"

    calls = [call(expected_execution_time), call(expected_memory_usage)]
    mock_print.assert_has_calls(calls)

  @patch('debug.Debug.on', True)
  def test_infoDict(self):
    """디버그 정보 저장 테스트"""
    mocked_file = mock_open()
    with patch('builtins.open', mocked_file, create=True):
      with open(self.TEST_FILENAME, 'w') as f:
        Debug.infoDict(f, self.TEST_DICT)

    mocked_file().write.assert_any_call("key1: value1\n")
    mocked_file().write.assert_any_call("key2: value2\n")

  @patch('debug.Debug.on', True)
  def test_infoList(self):
    """디버그 정보 저장 테스트"""
    mocked_file = mock_open()
    with patch('builtins.open', mocked_file, create=True):
      with open(self.TEST_FILENAME, 'w') as f:
        Debug.infoList(f, self.TEST_LIST)

    mocked_file().write.assert_any_call("item1, item2\n")
    mocked_file().write.assert_any_call("item3, item4\n")

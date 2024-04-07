import re
import unittest
import kiwipiepy
from unittest.mock import patch, mock_open, MagicMock
from kiwipiepy import Kiwi, Token

from app import RegProcessor, KiwiProcessor
from libs.const import *
from libs.debug import *


class TestRegProcessor(unittest.TestCase):

  def setUp(self):
    # Given
    self.TEST_CONTENT = "홍익대학교부속여자중학교는 부산중앙중학교 옆이다"
    self.RETURN_VALUE = [('홍익대학교부속여자중학교', '중학교'), ('부산중앙중학교', '중학교')]
    self.EXPECTED = [key[0] for key in self.RETURN_VALUE]

  def test_정규식분석_디버그모드_활성(self):

    with patch('libs.debug.Debug.on', True), \
         patch('builtins.open', mock_open(), create=True) as mocked_file, \
         patch('re.findall', return_value=self.RETURN_VALUE) as mocked_findall:

      # when
      result = RegProcessor.find(self.TEST_CONTENT)

      # then
      mocked_file.assert_called_once_with(DEBUG_SEARCH_FILE,
                                          'w',
                                          encoding='utf-8')
      mocked_findall.assert_called_once_with(REGEX_GREEDY_PATTERN,
                                             self.TEST_CONTENT)
      self.assertEqual(result, self.EXPECTED)

  def test_정규식분석_디버그모드_비활성(self):

    with patch('libs.debug.Debug.on', False), \
         patch('re.findall', return_value=self.RETURN_VALUE) as mocked_findall:

      # when
      result = RegProcessor.find(self.TEST_CONTENT)

      # then
      mocked_findall.assert_called_once_with(REGEX_GREEDY_PATTERN,
                                             self.TEST_CONTENT)
      self.assertEqual(result, self.EXPECTED)

  def test_정규식_findall(self):

    with patch('libs.debug.Debug.on', False), \
        patch('re.findall', return_value = self.RETURN_VALUE) as mocked_findall:

      # when
      result = RegProcessor._RegProcessor__findall(self.TEST_CONTENT)

      # then
      mocked_findall.assert_called_once_with(REGEX_GREEDY_PATTERN,
                                             self.TEST_CONTENT)
      self.assertEqual(result, self.EXPECTED)

  def test_정규식검증(self):

    expected = re.search(VALID_PATTERN, self.TEST_CONTENT)
    with patch('re.search', return_value=expected) as mocked_search:
      # when
      result = RegProcessor.search(self.TEST_CONTENT)

      # then
      mocked_search.assert_called_once_with(VALID_PATTERN, self.TEST_CONTENT)
      self.assertEqual(result, expected)


# Mock Class
class MockToken:

  def __init__(self, form, tag):
    self.form = form
    self.tag = tag


class TestKiwiProcessor(unittest.TestCase):

  @patch('kiwipiepy.Kiwi')
  def setUp(self, MockKiwi):

    # Kiwi 객체를 모킹하여 테스트 환경 설정
    self.mock_kiwi = MockKiwi.return_value
    self.mock_kiwi.load_user_dictionary.return_value = None
    self.processor = KiwiProcessor()

  def test_빈목록_검증(self):

    # then
    result = self.processor.find(None)
    self.assertEqual(result, [])

  @patch('libs.debug.Debug.on', True)
  @patch('builtins.open', new_callable=MagicMock)
  def test_분석_디버그모드_활성(self, mocked_open):

    # Given
    verify = ['서울고등학교']
    expected = ['서울고등학교']
    token1 = MagicMock(spec=kiwipiepy.Token, form='서울', tag='NNP')
    token2 = MagicMock(spec=kiwipiepy.Token, form='고등학교', tag='NNG')
    self.mock_kiwi.tokenize.return_value = [token1, token2]

    # when
    result = self.processor.find(verify)

    # then
    self.assertEqual(result, expected)
    mocked_open.assert_called_once_with(DEBUG_ANALYZE_FILE,
                                        'w',
                                        encoding='utf-8')
    self.mock_kiwi.tokenize.assert_called_once()

  @patch('libs.debug.Debug.on', False)
  def test_분석_디버그모드_비활성(self):

    # Given
    verify = ['서울고등학교']
    expected = ['서울고등학교']
    token1 = MagicMock(spec=kiwipiepy.Token, form='서울', tag='NNP')
    token2 = MagicMock(spec=kiwipiepy.Token, form='고등학교', tag='NNG')
    self.mock_kiwi.tokenize.return_value = [token1, token2]

    # when
    result = self.processor.find(verify)

    # then
    self.assertEqual(result, expected)
    self.mock_kiwi.tokenize.assert_called_once()

  @patch('libs.debug.Debug.on', False)
  def test_명사가_아닌_품사(self):
    """‘금곡/NNP’+‘초등학교/NNG’+‘에/EC’
            명사가 아닌 품사(EC)가 포함된 경우, ‘금곡초등학교’ 추출"""

    # Given
    verify = ['금곡초등학교는']
    expected = ['금곡초등학교']
    token1 = MagicMock(spec=kiwipiepy.Token, form='금곡', tag='NNP')
    token2 = MagicMock(spec=kiwipiepy.Token, form='초등학교', tag='NNG')
    token3 = MagicMock(spec=kiwipiepy.Token, form='는', tag='EC')
    self.mock_kiwi.tokenize.return_value = [token1, token2, token3]

    # when
    result = self.processor.find(verify)

    # then
    self.assertEqual(result, expected)
    self.mock_kiwi.tokenize.assert_called_once()

  @patch('libs.debug.Debug.on', False)
  def test_고가_MM품사_조사같이(self):
    """‘국제/NNG’+‘예술/NNG’+‘고/MM’+‘에//EC’’
            명사가 아닌 품사(EC)가 포함된 경우, ‘국제예술고’ 추출"""

    # Given
    verify = ['국제예술고에']
    expected = ['국제예술고']
    token1 = MagicMock(spec=kiwipiepy.Token, form='국제', tag='NNG')
    token2 = MagicMock(spec=kiwipiepy.Token, form='예술', tag='NNG')
    token3 = MagicMock(spec=kiwipiepy.Token, form='고', tag='MM')
    token4 = MagicMock(spec=kiwipiepy.Token, form='에', tag='EC')
    self.mock_kiwi.tokenize.return_value = [token1, token2, token3, token4]

    # when
    result = self.processor.find(verify)

    # then
    self.assertEqual(result, expected)
    self.mock_kiwi.tokenize.assert_called_once()

  def test_한단어_NNP(self):
    """‘서울고등학교/NNP’ 고유명사가 분석된 경우"""
    # when
    tokens = [MockToken('서울고', 'NNP')]
    result = self.processor._KiwiProcessor__only_nnp(tokens)

    # then
    self.assertTrue(result)

  def test_한단어_NNG(self):
    """‘금고/NNG’ 일반명사가 분석된 경우"""
    # when
    tokens = [MockToken('금고', 'NNG')]
    result = self.processor._KiwiProcessor__only_nnp(tokens)

    # then
    self.assertFalse(result)

  def test_여러단어_시작글자_NNP(self):
    """‘서울/NNP’+‘고등학교/NNG’ 분석된 경우"""
    # when
    tokens = [MockToken('서울', 'NNP'), MockToken('고등학교', 'NNG')]
    result = self.processor._KiwiProcessor__startwith_nnp_and_nouns(tokens)

    # then
    self.assertTrue(result)

  def test_여러단어_시작글자_NNG(self):
    """‘국제/NNG’+‘고등학교/NNG’ 분석된 경우"""
    # when
    tokens = [MockToken('국제', 'NNG'), MockToken('고등학교', 'NNG')]
    result = self.processor._KiwiProcessor__startwith_nng_and_nouns(tokens)

    # then
    self.assertTrue(result)

  def test_여러단어_시작글자_명사아님(self):
    """‘고/EC+‘국제/NNG’+‘고등학교/NNG’ 분석된 경우"""
    # when
    tokens = [
        MockToken('고', 'EC'),
        MockToken('국제', 'NNG'),
        MockToken('고등학교', 'NNG')
    ]
    result = self.processor._KiwiProcessor__startwith_nnp_and_nouns(tokens)

    # then
    self.assertFalse(result)

  def test_여러단어_명사추출_시작부분연속(self):
    """‘금곡/NNP+‘초등학교/NNG’+‘는/EC’ 분석된 경우"""
    # when
    tokens = [
        MockToken('금곡', 'NNP'),
        MockToken('초등학교', 'NNG'),
        MockToken('는', 'EC')
    ]
    match = self.processor._KiwiProcessor__concat_nnp_nng(tokens)

    # then
    self.assertEqual(match.group(), '금곡초등학교')

  def test_여러단어_명사추출_연속안됨(self):
    """‘서울/NNP+‘고/EC+‘고등학교/NNG’ 분석된 경우, 단어추출 없음"""
    # when
    tokens = [
        MockToken('서울', 'NNP'),
        MockToken('고', 'EC'),
        MockToken('고등학교', 'NNG')
    ]
    match = self.processor._KiwiProcessor__concat_nnp_nng(tokens)

    # then
    self.assertIsNone(match)

  def test_여러단어_명사추출_명사한개(self):
    """‘고/EC+‘고등학교/NNG’ 분석된 경우, 단어추출 없음"""
    # when
    tokens = [MockToken('고', 'EC'), MockToken('고등학교', 'NNG')]
    match = self.processor._KiwiProcessor__concat_nnp_nng(tokens)
    # then
    self.assertIsNone(match)

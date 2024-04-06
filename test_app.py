import os
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from kiwipiepy import Kiwi, Token
from app import RegProcessor, KiwiProcessor
from libs.const import *

class TestRegProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = RegProcessor()

    @patch('app.re.findall')
    def test_findall(self, mock_findall):
        with patch.dict(os.environ, {"DEBUG": "off"}):        
            mock_findall.return_value = [('School', 'dummy')]
            text = "School test School"
            
            result = self.processor.findall(text)
            mock_findall.assert_called_once_with(greedy_pattern, text)
            self.assertEqual(result, ['School'])

class TestKiwiProcessor(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('app.kiwipiepy.Kiwi')
        self.mock_kiwi_class = self.patcher.start()
        self.mock_kiwi = self.mock_kiwi_class.return_value
        self.mock_kiwi.load_user_dictionary.return_value = None       
        self.processor = KiwiProcessor()

    @patch('kiwipiepy.Kiwi')
    def test_analyze(self, MockKiwi):
        with patch.dict(os.environ, {"DEBUG": "off"}):    
            mock_kiwi_instance = MockKiwi.return_value
            mock_token = MagicMock()
            mock_token.form = 'School'
            mock_token.tag = 'NNP'
            mock_token.start = 0
            mock_token.len = 6
            mock_kiwi_instance.tokenize.return_value = [mock_token]

            processor = KiwiProcessor()  # Kiwi 인스턴스는 내부적으로 목킹됨
            result = processor.analyze(['School'])
            
            mock_kiwi_instance.tokenize.assert_called_once_with('School')
            self.assertIn('School', result[0])

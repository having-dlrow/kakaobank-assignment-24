import os
from datetime import datetime
from collections import Counter
from libs.const import *

class FileHandler:
    @staticmethod    
    def read(filename):
        """데이터를 읽어서 반환합니다."""
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def save(data):
        """데이터를 파일(result.{date}.txt)에 저장합니다."""
        
        # 디렉토리가 존재하지 않으면 생성
        if not os.path.exists(RESULT_DIR):
            os.makedirs(RESULT_DIR)

        filename = f"{RESULT_DIR}/{RESULT_FILENAME}.{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for key, count in data:
                f.write(f"{key}\t{count}\n")

        return filename

class CounterProcessor:
    @staticmethod    
    def count(word):
        """텍스트에서 학교 이름을 찾아 빈도수를 계산합니다."""
        counts = Counter(word)
        return sorted(counts.items(), key=lambda item: item[1], reverse=True)
 

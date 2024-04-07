import os
from datetime import datetime
from collections import Counter

class FileHandler:

    def read(self, filename):
        """데이터를 읽어서 반환합니다."""
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    
    def write(self, filename, data):
        """데이터를 파일에 저장합니다."""
        with open(filename, 'w', encoding='utf-8') as f:
            for key, value in data:
                f.write(f"{key}\t{value}\n")

    def save(self, data, dirname, filename):
        """데이터를 파일에 저장합니다."""
        if self.is_dir(dirname) :
            filename = self.add_datetime(filename)
            self.write(filename, data)

        return filename
    
    def add_datetime(self, filename):
        """파일명에 현재 날짜와 시간을 추가합니다."""
        return f"{filename}.{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

    def is_dir(self, dirname):
        """디렉토리가 존재하지 않으면 생성합니다."""
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return True

class CounterHandler:

    def count(self, word):
        """텍스트에서 학교 이름을 찾아 빈도수를 계산합니다."""
        counts = Counter(word)
        return sorted(counts.items(), key=lambda item: item[1], reverse=True)
 

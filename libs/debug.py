import time
import os
from memory_profiler import memory_usage
from libs.const import *


DEBUG = os.environ.get('DEBUG') == 'on'  # 환경 변수를 통한 디버그 모드 설정

class Debug:
    start_time = None
    mem_usage_start = None

    @staticmethod
    def start():
        """메모리 및 실행시간을 계산합니다."""
        # if DEBUG:
        Debug.start_time = time.time()
        Debug.mem_usage_start = memory_usage()[0]

    @staticmethod
    def end():
        """메모리 및 실행시간을 계산합니다."""  
        if DEBUG:
            end_time = time.time()
            mem_usage_end = memory_usage()[0]
            print(f"Execution time: {end_time - Debug.start_time} seconds")
            print(f"Memory usage: {mem_usage_end - Debug.mem_usage_start} MiB")

    @staticmethod
    def token(file, word, tokens):
        """디버그 정보를 파일에 작성합니다."""
        if DEBUG:        
            file.write(f"word: {word} tokens: {tokens} \n")

    @staticmethod
    def reg(all_matches):
        """디버그 정보를 파일에 작성합니다."""
        if DEBUG:
            with open(DEBUG_SEARCH_FILE, 'w', encoding='utf-8') as f: 
                for str, str2, str3 in all_matches:
                    f.write(f"str1: {str}, str2: {str2} str3: {str3} \n")   
import time
import os
from memory_profiler import memory_usage


class Debug:
  start_time = None
  mem_usage_start = None
  on = None

  @staticmethod
  def is_on():
    if Debug.on is None:
      Debug.on = os.environ.get('DEBUG') == 'on'
    return Debug.on  # 환경 변수를 통한 디버그 모드 설정

  @staticmethod
  def start():
    """메모리 및 실행시간을 계산합니다."""
    if Debug.is_on():
      Debug.start_time = time.time()
      Debug.mem_usage_start = memory_usage()[0]

  @staticmethod
  def end():
    """메모리 및 실행시간을 계산합니다."""
    if Debug.is_on():
      end_time = time.time()
      mem_usage_end = memory_usage()[0]
      print(f"Execution time: {end_time - Debug.start_time} seconds")
      print(f"Memory usage: {mem_usage_end - Debug.mem_usage_start} MiB")

  @staticmethod
  def infoDict(file, dict):
    """디버그 정보를 파일에 작성합니다."""
    if Debug.is_on():
      for key, value in dict.items():
        file.write(f"{key}: {value}\n")

  @staticmethod
  def infoList(file, list):
    """디버그 정보를 파일에 작성합니다."""
    if Debug.is_on():
      for match in list:
        # 각 항목의 요소를 문자열로 변환하여 콤마로 구분
        line = ", ".join(map(str, match))
        file.write(line + "\n")

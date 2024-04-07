# 파일 및 환경 설정
RES_DIR = 'resource'
RESULT_DIR = 'result'
RESULT_FILENAME = f"{RESULT_DIR}/result"

RESOURCE_FILE = f"{RES_DIR}/comments.csv"
USER_DICT_FILE = f"{RES_DIR}/userDict.txt"

DEBUG_SEARCH_FILE = f"{RESULT_DIR}/log_search.log"
DEBUG_ANALYZE_FILE = f"{RESULT_DIR}/log_analyze.log"

# 검색할 단어 설정
non_greedy_words = ['고등학교', '국제학교', '예술학교', '중학교', '초등학교']
greedy_words = ['대학교', '고', '중', '초']

# 정규 표현식 패턴 설정
non_greedy_include = '|'.join(non_greedy_words)
greedy_include = '|'.join(greedy_words)

REGEX_GREEDY_PATTERN = rf"([가-힣]+?({non_greedy_include})|[가-힣]+({greedy_include}))"  # Regex 검색 패턴
VALID_PATTERN = rf"([가-힣]+({non_greedy_include})|[가-힣]+({greedy_include}))"  # Kiwipiepy 분석 단어, 검증용

# 포함 형태소
NNP = 'NNP'
NNG = 'NNG'
NNB = 'NNB'
MM = 'MM'
TOKEN_TAGS_TO_CHECK = [NNP, NNG, NNB, MM]

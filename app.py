import re
import kiwipiepy
from libs.debug import *
from libs.handler import FileHandler, CounterHandler
from libs.const import *

class RegProcessor:

    @staticmethod
    def find(text):
        """실행 Wrapper""" 
        if DEBUG:
            with open(DEBUG_SEARCH_FILE, 'w', encoding='utf-8') as f:
                return RegProcessor.__findall(text, f)
        else :
            return RegProcessor.__findall(text)

    @staticmethod
    def __findall(text, f = None):
        """전체에서 단어를 추출합니다."""
        all_matches = re.findall(greedy_pattern, text)
        if DEBUG:
            Debug.infoList(f, all_matches)
        
        # findall은 튜플의 리스트를 반환, 각 튜플의 첫 번째 요소만 추출
        return [key[0] for key in all_matches]
    
    @staticmethod
    def search(text):
        """단어 Match 여부를 반환합니다."""
        return re.search(non_greedy_pattern, text)    

class KiwiProcessor:
    def __init__(self):
        self.kiwi = kiwipiepy.Kiwi(typos=None)
        self.kiwi.load_user_dictionary(USER_DICT_FILE)

    def __only_nnp(self, tokens):
        """고유명사이며, 한개의 단어인 경우"""
        return len(tokens) == 1 and tokens[0].tag == NNP

    def __startwith_nnp_and_nouns(self, tokens):
        """고유명사로 시작하는 경우"""
        return (tokens[0].tag == NNP and 
                all(token.tag in TOKEN_TAGS_TO_CHECK for token in tokens[1:]))

    def __startwith_nng_and_nouns(self, tokens):
        """일반명사로 시작하는 경우"""
        return (tokens[0].tag == NNG and 
                all(token.tag in TOKEN_TAGS_TO_CHECK for token in tokens[1:]))

    def __concat_nnp_nng(self, tokens):
        """연속된 NNP, NNG, NNB, MM 토큰을 합칩니다."""
        temp = ''
        for i, token in enumerate(tokens):
            # 현재 토큰, 이전 토큰이 TAGS_TO_CHECK 해당 하는 경우
            if (token.tag in TOKEN_TAGS_TO_CHECK and
                (i > 0 and tokens[i-1].tag in TOKEN_TAGS_TO_CHECK)):
                temp += token.form
            else:
                # 초기화
                if temp:
                    temp = ''
                # 재시작
                if token.tag in TOKEN_TAGS_TO_CHECK:
                    temp = token.form

        return RegProcessor.search(temp)

    def __extract(self, analyzed_results, tokens):
        """단어 리스트를 분석하여 이름을 추출합니다."""
        if self.__only_nnp(tokens):
            # ex. 양덕여자중학교
            analyzed_results.append(tokens[0].form)
        elif len(tokens) > 1:
            if self.__startwith_nnp_and_nouns(tokens):
                # ex. 경기국제통상고등학교  
                nouns_only_sentence = ''.join(token.form for token in tokens)
                analyzed_results.append(nouns_only_sentence)

            elif self.__startwith_nng_and_nouns(tokens):
                # ex. 여자고등학교, 국제고등학교, 국립전통예술학교
                nouns_only_sentence = ''.join(token.form for token in tokens)
                analyzed_results.append(nouns_only_sentence)

            else:
                # ex. 진짜동두천여자중학교 -> 동두천여자중학교 (추출)
                matched = self.__concat_nnp_nng(tokens)
                if matched:
                    analyzed_results.append(matched.group())

        return analyzed_results

    def __analyze(self, words, f = None):
        """단어 리스트를 분석하여 이름을 추출합니다.""" 
        results = []
        for word in words:
            tokens = self.kiwi.tokenize(word)                           # 분석
            if DEBUG:
                Debug.infoDict(f, {word : tokens})
            self.__extract(results, tokens)                             # 분류
        return results

    def find(self, words):
        """실행 Wrapper"""
        if words is None:
            print("No words provided to KiwiProcessor.find method")
            return []
             
        if DEBUG:
            with open(DEBUG_ANALYZE_FILE, 'w', encoding='utf-8') as f:
                return self.__analyze(words, f)
        else :
            return self.__analyze(words)

if __name__ == "__main__":
    
    # pre
    Debug.start()

    fh = FileHandler()
    kiwi = KiwiProcessor()
    doc = fh.read(RESOURCE_FILE)

    # process
    founds = RegProcessor.find(doc)                                     # 추출
    words = kiwi.find(founds)                                           # 분석 & 분류

    # after
    fh.save(CounterHandler().count(words), RESULT_DIR, RESULT_FILENAME)
    Debug.end()

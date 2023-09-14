import re #정규 표현식
from speak import speak #(내부 모듈)시리 음성


#단순 대답 함수
def small_talk(order):

    #상황에 맞는 대답 딕셔너리
    talks={
        '안녕': '안녕하세요. 오늘도 화이팅입니다',
        '바보|답답|못 알아': '죄송합니다',
        '메롱': '놀리지 마세요',
        '고마워': '별 말씀을요',
        '아침': '좋은 아침입니다',
        '아니야|잘못': '언제든 다시 불러주세요'
    }

    #대답 고르기
    for talk in talks:
        if re.search(talk, order) != None : return speak(talks[talk]) 
    
    

from siri import Siri #(내부 모듈)시리 부르기

#사용자 정보. 사용자 정보 수정 시 다른 내부 코드를 건드릴 필요 없도록 바깥 코드에서 주어지는 형태로 구성.
user = {
    'assitant_name': '시리',
    'api_weather': 'yn1pMbW2aeAxRfNyFVCou45Z79AltuIbdPg+nJgrM7tbpSiHnuJinR4klbVieo+VcZDtE5I0zqPlezcLkAzAfA==',
    'api_word': 'F6A963DE635B07C8D211C4B83D7D6947'
    }

siri_of_user=Siri(user) #시리 객체 생성
siri_of_user.siri_start() #시리 작동 함수



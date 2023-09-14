import requests #요청을 하기 위한 모듈
import json  #json파일을 다루기 위한 모듈
import random #랜덤 함수 사용을 위한 모듈
from speak import speak #(내부 모듈)시리 음성
from voice_input import voice #(내부 모듈)사용자 음성 인식

#게임 클래스
class Game:
    def __init__(self, api):
        self.api = api

    #단어 검색
    def search_word(self, input_word, method): #검색 키워드, 검색 방식 인자
        word=input_word.encode('utf-8') #한글 인코딩
        params = {
            'key': self.api,
            'req_type': 'json',
            'q': word,  #검색어
            'advanced': 'y',
            'pos': 1, #명사
            'letter_s': 2, #2글자 이상
            'letter_e':10, #10글자 이하
            'method': method, #검색 방식
            'type3': 'general', #표준어만
            'num':50 #50개의 검색결과
            }

        try:
            response = requests.get('https://opendict.korean.go.kr/api/search', verify=False, params=params)  #검색 정보 받기
            data = json.loads(response.text)  #문자열을 딕셔너리로 변환
            return data['channel']['item']  #단어가 담긴 부분만 리스트로 반환
        except ConnectionError:
            print('통신 장애')


    #끝말잇기 게임
    def word_game(self):
        speak('끝말잇기 게임을 시작합니다. 단어를 제시하세요.')
        siri = '가'
        counts = 0
        user = ''
        stack=[]
        
        while True:  #한 쪽이 질 때까지 시행

            #유저가 단어 말하기
            user = voice(5, 2, 0)  
                        #유저의 단어 체크
            if user.count("그만") != 0 | user.count('내가 졌'): #중간에 그만두기
                print('좋은 시간이었어요')
                break
            if (len(user)<=1)|((siri[-1]!=user[0])&counts!=0): #사용자가 잘못 말했을 때
                speak('다시 말씀해주세요')
                continue
            len_result = len(self.search_word(user, 'exact'))  #사용자가 말한 단어가 사전에 있는지 확인
                        #말한 단어 저장
            stack.append(user)  
            count += 1

            #사용자가 졌을 때(사용자가 말한 단어가 사전에 없거나, 이전에 나왔던 단어일 때)
            if len_result == 0 |stack.count(user)!=0: 
                speak('제가 이겼습니다')
                break
            
            #시리가 답변할 단어 검색
            siri_raw = self.search_word(user[-1], 'start')
            #말한 단어 저장
            stack.append(siri_raw)  
            #시리가 답변할 단어가 없어서 사용자가 이겼을 때
            if len(siri_raw) == 0: 
                speak('당신이 이겼습니다')
                break
            #시리가 대답하기
            for word in siri_raw: #이미 말한 단어인 경우 답할 목록에서 제외
                if stack.count(word) != 0:
                    siri_raw.remove(word)
            siri_answer=random.choice(siri_raw)['word'].replace('-', '') #받은 리스트에서 아무거나 고르기
            speak(siri_answer)  


    #업다운 게임                        
    def up_down(self):
        speak('업다운 게임을 시작합니다. 10회 안에 맞춰보세요. 1~100 사이 숫자입니다.')
        hidden_number = int(random.randint(1, 100))  #랜덤 숫자 생성
        
        #사용자 음성 인식
        def listen():
            try:
                player_raw = voice()
                player = int(player_raw)
                return player
            except TypeError:
                return listen()
            except ValueError: #한 음절 숫자 인식 에러 처리
                if player_raw == '일':
                    return 1
                elif player_raw == '이':
                    return 2
                elif player_raw == '삼':
                    return 3
                elif player_raw == '사':
                    return 4
                elif player_raw == '오':
                    return 5
                elif player_raw == '육':
                    return 6
                elif player_raw == '칠':
                    return 7
                elif player_raw == '팔':
                    return 8
                elif player_raw == '구':
                    return 9
                elif (player_raw == '백')|(player_raw =='뱅'):
                    return 100
                else:
                    print('인식 실패')
                    return listen()
        
        #up down 판정
        for i in range(10):                   
            player = listen()       
            if player==hidden_number:
                speak("정답입니다.")
                break
            elif player<hidden_number:
                speak("up")
            else :
                speak("down.")
            if i==9:
                speak("실패했습니다.")

    #게임 선택
    def games(self, order):
        if order.count('끝말잇기') != 0:
            self.word_game()
        elif order.count('업다운') != 0:
            self.up_down()

    #게임 선택으로 들어가기
    def game_choice(self, order):  
        if (order.count('끝말잇기') | (order.count('업')&order.count('다운'))) == 0:
            speak('어떤 게임을 하시겠어요?')
            gc=voice()
            if (gc.count('끝말잇기') | gc.count('업')&gc.count('다운')) == 0:
                speak('이해하지 못했어요')
            else:
                self.games(order)
        else :
            self.games(order)

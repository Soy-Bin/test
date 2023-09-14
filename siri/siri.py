import re #정규 표현식 사용 모듈
from speak import speak #(내부 모듈)시리 음성
from service import Service #(내부 모듈)기능
from game import Game #(내부 모듈)게임
from voice_input import voice  #(내부 모듈)사용자 음성 인식
from weather import Weather #(내부 모듈)날씨 정보
from small_talk import small_talk #(내부 모듈)단순 대답


#시리 작동 클래스
class Siri:
	def __init__(self, user):
		self.name=user['assitant_name'] #사용자 이름 저장
		self.weather = Weather(user['api_weather']) #날씨 인스턴스 생성. 사용자 날씨 api key 전달
		self.games = Game(user['api_word']) #게임 인스턴스 생성. 사용자 단어 검색 api key 전달
		self.service = Service()  #서비스 인스턴스 생성
		
		#서비스 메뉴 딕셔너리python siri.py
		self.services = {
			'exchange':{'checker':'환율','need_arg':False, 'method':self.service.exchange},
			'time_is':{'checker':'지금 (시|몇)','need_arg':False, 'method':self.service.time_is},
		    'weather':{'checker':'날씨','need_arg':True, 'method':self.weather.weather},
		    'fine_dust':{'checker':'미세|먼지','need_arg':True, 'method': self.weather.fine_dust},
		    'games':{'checker':'게임|끝말잇기|심심|업(| )다운','need_arg':True, 'method':self.games.game_choice},
			'small_talk':{'checker':'안녕|바보|답답|못 알아|메롱|고마워|아침|아니야|잘못','need_arg':True, 'method':small_talk},
		    'service':{'checker':'(검색|뭐|무슨|궁금)|(야|어|때|돼|지|니|까|줘)$','need_arg':True, 'method':self.service.search},
			}


	#기능 선택하기
	def select(self, order):

		#사용자 명령어와 서비스 매칭 후 실행
		for service in self.services.keys():
			
			if re.search(self.services[service]['checker'], order) != None:
				if self.services[service]['need_arg'] == True:
					return self.services[service]['method'](order) #기능 실행
				else:
					return self.services[service]['method']() #기능 실행
		
		speak('이해할 수 없습니다')


	#시리 시작 함수
	def siri_start(self):
		
		while True:  #대기 상태
			
			#사용자 음성 인식
			is_siri=voice(0,2,1) 
			if is_siri.count(self.name) ==0 :  #시리를 불렀을 때 continue 아래 코드 실행
				continue
			print(is_siri)
			speak('무엇을 도와드릴까요?')
			#사용자 명령 인식 후 기능 선택 함수 호출
			self.select(voice())

		
		

		


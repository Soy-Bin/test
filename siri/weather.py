import requests  #요청을 하기 위한 모듈
import json #json파일을 다루기 위한 모듈
import speech_recognition as sr  #음성 인식 모듈
from speak import speak  #(내부모듈)시리 음성
from gps import ip_gps, to_gps #(내부 모듈)위치 정보


#날씨 관련 클래스
class Weather:
    def __init__(self, api):
        self.api= api
        self.gps=ip_gps() #위치 정보 얻기


    #GPS 추출 함수
    def get_location(self, order, what_for):
        order_info = order.split(what_for)[0]
        if (order_info=='오늘')|(order_info=='지금')|(order_info=='현재')|(order_info=='') : #현재 위치의 gps
            gps = {'location':'오늘','lat': self.gps['lat'], 'long': self.gps['long']}
        else:                                                                             #원하는 지역의 gps
            gps = to_gps(order_info)
        return gps

    
    #일기 예보 기능
    def weather(self, order):
        
        #기상 정보 코드
        WMO={0:'맑습', 1:'대체로 맑습', 2:'약간 흐립', 3:'흐립', 45:'안개가 낍', 48:'서리가 내립',51:'이슬비가 내립', 53:'이슬비가 내립', 55 :'이슬비가 내립', 
        56:'진눈깨비가 내립', 57:'진눈깨비가 내립', 61 : '비가 약간 내립', 63:'비가 내립', 65:'비가 많이 내립', 66: '어는 비가 약간 내립', 67:'어는 비가 많이 내립',
        71:'눈이 약간 내립', 73:'눈이 내립', 75:'눈이 많이 내립', 77: '싸락눈이 내립', 80:'소나기가 약간 내립', 81:'소나기가 내립', 82:'소나기가 많이 내립',
        85:'눈소나기가 약간 내립', 86:'눈소나기가 많이 내립', 95:'뇌우가 내립', 96:'뇌우와 우박이 약간 내립', 99:'뇌우와 우박이 많이 내립'
        }

        #위치 정보 get
        gps = self.get_location(order, ' 날씨')
        
        #오늘 날씨 정보 얻어오기
        response=requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={gps['lat']}&longitude={gps['long']}&daily=weathercode,temperature_2m_max,temperature_2m_min&current_weather=true&timezone=GMT&forecast_days=1") 
        #json 파일을 텍스트로 저장
        data = json.loads(response.text)
        
        #날씨 정보 추출
        cel_high=data['daily']['temperature_2m_max'][0] #최고 기온
        cel_low=data['daily']['temperature_2m_min'][0] #최저 기온
        today_wmo = WMO[data['daily']['weathercode'][0]]  #기상 정보
        

        #날씨 정보 출력
        speak(gps['location']+f' 날씨는 최고 기온 {cel_high}도, 최저 기온 {cel_low}도, {today_wmo}니다.')



    #미세 먼지 기능
    def fine_dust(self, order):
        gps = ip_gps()  #위치 정보 받기

        #지역 코드
        regions = {'Seoul': '서울', 'Busan': '부산', 'Daegu': '대구', 'Incheon': '인천', 'Gwangju': '광주', 'Daejeon': '대전', 'Ulsan': '울산', 'Sejong': '세종', 'Gyeonggi-do': '경기',
        'Gangwon-do':'강원','Chungcheongbuk-do':'충북','Chungcheongnam-do':'충남','Jeonbuk':'전북','Jeonnam':'전남','Gyeongbuk':'경북','Gyeongnam':'경남','Jeju':'제주'}
        
        #요청 파라미터
        params = {
        'serviceKey': self.api,
        'returnType': 'json',
        'numOfRows': '100',
        'pageNo': '1',
        'sidoName': regions[gps['region']],
        'dataTerm':'DAILY',
        'ver': '1.0',
        }
        response = requests.get('http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty', params=params) #대기오염정보 요청
        data_all = json.loads(response.text)  #문자열을 자료 구조로 변환
     
        try:
            pm10_grade=int(data_all['response']['body']['items'][0]['pm10Grade']) #미세먼지 단계
            pm10_val=int(data_all['response']['body']['items'][0]['pm10Value'])
            pm10='' #환경 기준 판단값
            if pm10_grade==1: #환경 기준 판단
                pm10='좋음'
            elif pm10_grade==2:
                pm10='보통'
            elif pm10_grade==3:
                pm10='나쁨'
            elif pm10_grade==4:
                pm10='매우 나쁨'
            speak(f"오늘의 미세먼지 농도는 {pm10_val}, {pm10}입니다.")
        except ValueError:
            print('통신 장애')




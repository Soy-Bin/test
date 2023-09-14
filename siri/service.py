import requests #요청을 하기 위한 모듈
import json #json파일을 다루기 위한 모듈
from selenium import webdriver #인터넷 창을 켜기 위한 모듈
from selenium.webdriver.common.by import By #인터넷 창에서 요소를 찾아주는 모듈
from selenium.webdriver.support.ui import WebDriverWait #웹드라이버 행동을 기다려주는 모듈
from selenium.webdriver.support import expected_conditions as EC  #Webdriverwait모듈에 필요한 값을 넣는 모듈
from selenium.webdriver.chrome.options import Options #셀레늄 옵션
import time  #시간 모듈
from bs4 import BeautifulSoup
from speak import speak  #(내부 모듈)시리 음성


#서비스 기능 클래스
class Service:
    def __init__(self):
        pass

    #검색 기능
    def search(self, order):
    
        #필요 없는 단어 지우기
        order=order.replace('지금 ', '')
        #검색어 가공
        if order.count('검색') != 0:
            word = order.split(' 검색')[0]
        elif order.count('가 ')!=0:           #조사 기준으로 앞 부분만 추출
            word = order.split('가 ')[0]
        elif order.count('이 ')!=0:
            word = order.split('이 ')[0]
        elif order.count('은 ')!=0:
            word = order.split('은 ')[0]
        elif order.count('는 ')!=0:
            word = order.split('는 ')[0]
        elif order.count('어떻') != 0:        #조사 없이 말하는 경우 몇 가지
            word = order.split(' 어떻')[0]
        elif order.count('어때') != 0:
            word = order.split(' 어때')[0]
        elif order.count('궁금') != 0:
            word = order.split(' 궁금')[0]
        else: #그 외 문장 구조인 경우 통으로 검색
            word = order
        
        speak(f'{word} 검색을 시작합니다')

        #창 꺼지지 않는 옵션 설정
        options = Options()
        options.add_experimental_option("detach", True)      
        driver = webdriver.Chrome(options=options) #인터넷 창 드라이버 객체 생성
        #인터넷 창 열기
        driver.get('http://www.naver.com') 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#query')))#창이 완전히 열릴 때까지 대기하고, 찾고자 하는 요소를 찾으면 대기 중단
        #검색창 찾기
        serch_in=driver.find_element(By.CSS_SELECTOR, '#query') 
        #검색어 입력
        serch_in.send_keys(word)
        #검색 버튼 찾기
        search_button=driver.find_element(By.CSS_SELECTOR, '#search-btn')
        #검색 버튼 누르기
        search_button.click()



    #환율 정보
    def exchange(self):
        response = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%99%98%EC%9C%A8')
        soup = BeautifulSoup(response.text, 'html.parser')
        exchange=soup.select('#_cs_foreigninfo > div:nth-child(1) > div.api_cs_wrap > div > div.c_rate > div.rate_bx > div.rate_spot._rate_spot > div.rate_tlt > h3 > a > span.spt_con.up > strong')
        
        exchange_value=exchange[0].text.split('.')[0]
        speak(f'오늘의 환율은 {exchange_value}원 입니다')


    #현재 시각 정보
    def time_is(self):
        times = time.ctime().split(' ')[3]
        this_time = times.split(':')
        speak(f'지금 시각은 {this_time[0]}시 {this_time[1]}분 입니다')


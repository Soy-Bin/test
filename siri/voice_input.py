import speech_recognition as sr  #음성 인식 모듈
from speak import speak  #(내부모듈)시리 음성
import time


#음성 입력 함수
def voice(time_out=3, time_limit=3, is_main=0):  #listen함수 time out 인자, time limit인자, 메인 대기 상태(1)와 아닌 상태(0) 구분 코드
    r = sr.Recognizer() # 인식을 위한 객체 생성
    mic = sr.Microphone() # 마이크 사용을 위한 객체 생성
    try:
        with mic as source:  # 마이크에 담긴 소리를 토대로 아래 코드 실행
            r.adjust_for_ambient_noise(source)  #잡음 제거
            if is_main == 1:  #시리 대기 상태
                audio = r.listen(source, phrase_time_limit=time_limit)  #무한 대기를 위해 timeout인자 없앰
            else:  #일반적인 입력
                print('인식 중')
                audio = r.listen(source, timeout=time_out, phrase_time_limit=time_limit)  # 해당 소리를 오디오 파일 형태로 변환.
    
        try: 
            user_voice = r.recognize_google(audio, language="ko-KR")  # 오디오를 토대로 음성 인식하여 문자열로
            if is_main == 0: #메인이 아닐 때만 음성을 프린트해줌
                print(user_voice)
            return user_voice #음성 문자열을 반환
        except sr.UnknownValueError:  #입력이 없음
            if is_main == 0:
                speak("다시 말씀해주세요")
            return voice(time_out, time_limit, is_main)  #voice에서 음성을 인식해서 돌려주는 값을 받아서 상위 함수로 돌려주어야 함
        except sr.RequestError: #서버 에러
            print("서버 에러 발생")

    except Exception:
        if is_main == 0:
            print("인식 실패")
        return voice(time_out, time_limit, is_main) #다시 입력 받기. voice에서 음성을 인식해서 돌려주는 값을 받아서 상위 함수로 돌려주어야 함

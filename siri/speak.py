from gtts import gTTS #글자를 음성으로 읽어주는 모듈
import playsound  #컴퓨터로 소리를 내주는 모듈
import os  #파일 관리 모듈

#시리 음성
def speak(input):
	print(input)
	tts = gTTS(text=input, lang='ko') # 함수 인자로 들어온 text 를 음성으로 변환
	tts.save('siri.mp3') # 변환된 음성을 mp3로 저장
	playsound.playsound('siri.mp3')  # 저장한 음성 파일을 재생
	os.remove('siri.mp3')  # 재생 후에는 해당 파일 삭제
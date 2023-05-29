import speech_recognition as sr
import os
from config import key_config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_config['google_api_path']
recognizer = sr.Recognizer()

with sr.Microphone() as source:
	print("Say something!")
	audio = recognizer.listen(source)

try:
	print("Google Speech Recognition thinks you said:")
	print(recognizer.recognize_google(audio, language='ko-KR'))
except sr.UnknownValueError:
	print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
	print(f"Could not request results from Google Speech Recognition service; {e}")

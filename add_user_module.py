import face_recognition
import time
import os
import picamera
import pickle
from tts_module import text_to_speech
from stt_module import speech_to_text
import shutil

# pickle 모듈 설치하기

'''
add_user.py
* 신규 유저 추가 모듈(인코딩 포함)

user_names: 기존 유저들 이름 목록
1. 유저별로 디렉토리 생성
2. 해당 디렉토리에 사진 10장, 인코딩 정보 저장
3. user_names에 새로 추가된 user 이름 추가
'''

def add_user():
	CAPTURE_COUNT = 10
	text_to_speech("이름을 말씀해주세요.")
	# STT
	username = speech_to_text()

	# load user name list
	try:
		with open('user_names.pickle', 'rb') as f:
			user_names = pickle.load(f)
	# if the file does not exist, initialize it as an empty list
	except FileNotFoundError:
		user_names = [] 

	if not os.path.isdir(f'./{username}'):
		while True:
			encoding_count = 0
			os.mkdir(f"./{username}")
			# Captured image name list
			user_images_select = []
			# encoding list
			known_face_encodings = []
			
			with picamera.PiCamera() as camera:
				camera.resolution = (640, 480)
				camera.start_preview()
				print('Capture start!!')
				text_to_speech("10초간 촬영을 시작합니다. 움직이지 마세요.")

				for i in range(CAPTURE_COUNT):
					# capture image(save)
					time.sleep(0.5)
					camera.capture(f'./{username}/{username}{i}.jpg')
					user_images_select.append(f"{username}{i}.jpg")
				
				camera.stop_preview()
				print("Capture complete!!")
				camera.stop_preview()
				
			# make encoding list
			for i in range(CAPTURE_COUNT):
				user_image = user_images_select[i]
				image = face_recognition.load_image_file(f"./{username}/{user_image}")
				face_encoding = face_recognition.face_encodings(image)

				# 하나의 얼굴 요소만 반영
				if face_encoding:
					known_face_encodings.append(face_encoding[0])
					encoding_count += 1
				else:
					print(f"{user_images_select[i]} not encoded!!")

			if encoding_count != 10:
				shutil.rmtree(f'./{username}')
				text_to_speech("다시 등록을 시작합니다. 움직이지 마세요.")
			else:
				break

		# encoding list dump
		with open(f'./{username}/known_face_encodings.pickle', 'wb') as f:
			pickle.dump(known_face_encodings, f)

		# new username append
		user_names.append(username)

		# user_names list dump
		with open('user_names.pickle', 'wb') as f:
			pickle.dump(user_names, f)
			
		text_to_speech(f"{username}님의 등록이 완료되었습니다.")
		
		return username

	else:
		text_to_speech("이미 존재하는 유저입니다.")
		
		return username

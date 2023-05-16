import face_recognition
import time
import os
import picamera
import pickle

'''
add_user.py
* 신규 유저 추가 모듈(인코딩 포함)

user_names: 기존 유저들 이름 목록
1. 유저별로 디렉토리 생성
2. 해당 디렉토리에 사진 10장, 인코딩 정보 저장
3. user_names에 새로 추가된 user 이름 추가
'''

CAPTURE_COUNT = 10
# change to TTS, STT
username = input("Type your name: ")

# load user name list
with open('user_names.pickle', 'rb') as f:
	user_names = pickle.load(f)

if not os.path.isdir(f'./{username}'):
	os.mkdir(f"./{username}")

	user_images_select = []
	known_face_encodings = []
	
	with picamera.PiCamera() as camera:
		camera.resolution = (640, 480)
		camera.start_preview()
		print("Capture start!!")

		for i in range(CAPTURE_COUNT):
			# capture image(save)
			time.sleep(1)
			camera.capture(f'./{username}/{username}{i}.jpg')
			user_images_select.append(f"{username}{i}.jpg")
		
		print("Capture complete!!")

	# make encoding list
	for i in range(CAPTURE_COUNT):
		user_image = user_images_select[i]
		image = face_recognition.load_image_file(f"./{username}/{user_image}")
		face_encoding = face_recognition.face_encodings(image)

		if face_encoding:
			known_face_encodings.append(face_encoding[0])
		else:
			print(f"{user_images_select[i]} not encoded!!")

	# encoding list dump
	with open(f'./{username}/known_face_encodings.pickle', 'wb') as f:
		pickle.dump(known_face_encodings, f)

	# new username append
	user_names.append(username)

	# user_names list dump
	with open('user_names.pickle', 'wb') as f:
		pickle.dump(user_names, f)

else:
	print("Already exist user.")
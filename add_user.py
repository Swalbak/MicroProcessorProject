import time
import os
import picamera
import pickle

CAPTURE_COUNT = 10
# change to TTS, STT
username = input("Type your name: ")

if not os.path.isdir(f'./{username}'):
	os.mkdir(f"./{username}")

	user_images_select = []

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

	

	

else:
	print("Already exist user.")
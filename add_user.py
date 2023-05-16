import time
import picamera

CAPTURE_COUNT = 10
username = input("Type your name: ")
if
with picamera.PiCamera() as camera:
	camera.resolution = (640, 480)
	camera.start_preview()
	
	for i in range(CAPTURE_COUNT):
		time.sleep(1)
		camera.capture(f'jh{i}.jpg')


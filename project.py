import face_recognition
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

# 사용자들의 사진을 불러옵니다.
user_images_select = ["용빈.jpg", "지준.jpg", "jh1.jpg", "jh2.jpg"]
user_names_select = ["yongb 1", "jj 2", "jh", "jh"]
user_names = []

# 사용자들의 얼굴 인코딩을 저장할 리스트를 만듭니다.
known_face_encodings = []

# 각 사용자의 사진에서 얼굴 인코딩을 추출합니다.
for i in range(len(user_images_select)):
    user_image = user_images_select[i]
    image = face_recognition.load_image_file(user_image)
    face_encoding = face_recognition.face_encodings(image)
    if face_encoding:
        known_face_encodings.append(face_encoding[0])
        user_names.append(user_names_select[i])
    else:
        print(f"{user_images_select[i]} not encoded!!")

# PiCamera를 이용해 실시간으로 얼굴 인식을 진행합니다.
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))
camera.start_preview()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    # 현재 카메라에 찍힌 이미지에서 얼굴 부분을 인식합니다.
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for face_encoding in face_encodings:
        # 인식된 얼굴이 알려진 사용자들의 얼굴과 얼마나 유사한지 확인합니다.
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # 사용자가 일치하는 경우, 해당 사용자의 이름을 출력합니다.
        if True in matches:
            first_match_index = matches.index(True)
            name = user_names[first_match_index]

        print(f"The person in the video is: {name}")

    rawCapture.truncate(0)

    # 'q' 키를 누르면 루프에서 빠져나옵니다.
    

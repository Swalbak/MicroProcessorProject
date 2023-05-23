import face_recognition
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import pickle

'''
camera_main.py
* 만들어진 유저 인코딩을 가져와 누구인지 판별하는 모듈
'''

def face_detect():
    COUNT_NUM = 5
    before_name = 'unknown'
    count = 0

    # 사용자들의 사진을 불러옵니다.
    user_names = []

    # 사용자들의 얼굴 인코딩을 저장할 리스트를 만듭니다.
    known_face_encodings = []


    # PiCamera를 이용해 실시간으로 얼굴 인식을 진행합니다.

    # user name list
    with open('user_names.pickle', 'rb') as f:
        user_names_select = pickle.load(f)

    # make encoding list
    for user in user_names_select:
        with open(f'./{user}/known_face_encodings.pickle', 'rb') as f:
            encoding = pickle.load(f)
        known_face_encodings.extend(encoding)
        user_names.extend([user] * len(encoding))

    print("user_names", user_names)

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

            if name == before_name:
                count += 1                
            else:
                before_name = name
                count = 0

            if count == 5:
                return name
        
        rawCapture.truncate(0)

        

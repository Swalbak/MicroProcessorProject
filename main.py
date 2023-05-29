from config import key_config
import openai
import os
from tts_module import text_to_speech
from face_detect import face_detect
from add_user_module import add_user
from stt_module import speech_to_text
import pickle
from gpt_module import gpt_response
from sensor_monitoring_module import read_pir_sensor, read_ultrasonic_sensor

# ChatGPT API Key
openai.api_key = key_config['gpt_apikey']
# Google API Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_config['google_api_path']

pir_value = False
ultrasonic_dist = 100000

while True:
    pir_value = read_pir_sensor()
    ultrasonic_dist = read_ultrasonic_sensor()

    if pir_value and (ultrasonic_dist < 100):
        text_to_speech('안녕하세요! 얼굴인식 진행하겠습니다.')
        name = face_detect()

        if name == 'Unknown':
            text_to_speech("등록되지 않는 얼굴입니다. 새로 등록 시작하겠습니다.")
            name = add_user()

        text_to_speech(f'안녕하세요, {name}님! 무엇을 도와드릴까요?')
      
        messages = []
        if os.path.isfile(f'./{name}/messages.pickle'):
            with open(f'./{name}/messages.pickle', 'rb') as f:
                messages = pickle.load(f)
        else:
            messages = [{"role": "system", "content": f"안녕하세요, {name}님! 무엇을 도와드릴까요?"}]
        
        while True:
            # 사용자 거리 측정
            ultrasonic_dist = read_ultrasonic_sensor()

            if ultrasonic_dist > 50:
                text_to_speech("안녕히 가세요플레.")
                with open(f'./{name}/messages.pickle', 'wb') as f:
                    pickle.dump(messages, f)
                break
                
            # stt로 변경
            req = speech_to_text()
            
            messages.append({"role": "user", "content": req})
            messages, response = gpt_response(messages)
            text_to_speech(response)


from config import key_config
import openai
import os
from tts_module import text_to_speech
from face_detect import face_detect
from add_user_module import add_user
import pickle
from gpt_module import gpt_response
# ChatGPT API Key
openai.api_key = key_config['gpt_apikey']
# Google API Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_config['google_api_path']

# PIR Sensor
detection = True
# UltraSonic Sensor
dist = 10

while True:
    if detection and (dist < 50):
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
            if dist > 50:
                text_to_speech("안녕히 가세요플레.")
                with open(f'./{name}/messages.pickle', 'wb') as f:
                    pickle.dump(messages, f)
                break
                
            # stt로 변경
            stt = input("type your q: ")
            
            messages.append({"role": "user", "content": stt})
            messages, response = gpt_response(messages)
            text_to_speech(response)

'''
mmal: mmal_vc_port_enable: failed to enable port vc.null_sink:in:0(OPQV): ENOSPC
mmal: mmal_port_enable: failed to enable connected port (vc.null_sink:in:0(OPQV))0x5e83520 (ENOSPC)
mmal: mmal_connection_enable: output port couldn't be enabled
Traceback (most recent call last):
  File "/home/twentysix/MicroProcessorProject/main.py", line 25, in <module>
    name = add_user()
  File "/home/twentysix/MicroProcessorProject/add_user_module.py", line 44, in add_user
    with picamera.PiCamera() as camera:
  File "/usr/lib/python3/dist-packages/picamera/camera.py", line 433, in __init__
    self._init_preview()
  File "/usr/lib/python3/dist-packages/picamera/camera.py", line 512, in _init_preview
    self._preview = PiNullSink(
  File "/usr/lib/python3/dist-packages/picamera/renderers.py", line 558, in __init__
    self.renderer.inputs[0].connect(source).enable()
  File "/usr/lib/python3/dist-packages/picamera/mmalobj.py", line 2210, in enable
    mmal_check(
  File "/usr/lib/python3/dist-packages/picamera/exc.py", line 184, in mmal_check
    raise PiCameraMMALError(status, prefix)
picamera.exc.PiCameraMMALError: Failed to enable connection: Out of resources
'''

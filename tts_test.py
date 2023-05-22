from google.cloud import texttospeech
import os
from config import key_config

# Google API Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_config['google_api_path']

# Google Cloud Text-to-Speech 클라이언트 생성
client = texttospeech.TextToSpeechClient()

# 변환할 텍스트 지정
text = "안녕하세요!"
input_text = texttospeech.SynthesisInput(text=text)

# 음성 및 언어 설정
voice = texttospeech.VoiceSelectionParams(
    language_code="ko-KR",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

# 오디오 설정을 지정 - MP3
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# API 호출
response = client.synthesize_speech(
    input=input_text, 
    voice=voice, 
    audio_config=audio_config
)

# 출력을 MP3 파일로 저장
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
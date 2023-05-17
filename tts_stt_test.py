import sounddevice as sd
import numpy as np
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from google.cloud import texttospeech
import io
import os

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Record Audio
fs = 44100  # Sample rate
seconds = 5  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
myrecording = np.int16(myrecording * 32767.0)

# Audio content to send to the Speech-to-Text API
audio = types.RecognitionAudio(content=np.array(myrecording).tobytes())

# Speech-to-Text API config
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=fs,
    language_code='en-US')

# Detects speech in the audio file
response = speech.SpeechClient().recognize(config, audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=result.alternatives[0].transcript)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)

    os.system("mpg321 output.mp3")

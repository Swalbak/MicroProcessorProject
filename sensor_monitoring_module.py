import RPi.GPIO as GPIO
import time

# PIR 센서와 초음파 센서를 위한 핀 설정
PIR_PIN = 18 # 수정 필요
TRIG_PIN = 20 # 수정 필요
ECHO_PIN = 21 # 수정 필요

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def read_pir_sensor(queue):
    pir_value = GPIO.input(PIR_PIN)
    time.sleep(1)

    return pir_value

def read_ultrasonic_sensor(queue):
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.01)

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    time.sleep(1)

    return distance
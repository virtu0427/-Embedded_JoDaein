#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import time
led_R = 20 ; led_Y = 21 ;sensor = 4 # 노란색 LED, 빨간색 LED, 센서 입력핀 번호 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_R, GPIO.OUT) ; GPIO.setup(led_Y, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)
print ("PIR Ready . . . . ")
time.sleep(5) # PIR 센서 준비 시간
try:
while True:
if GPIO.input(sensor) == 1: #센서가 High(1)출력 , 움직임이 감지
GPIO.output(led_Y, 1) # 노란색 LED 켬
GPIO.output(led_R, 0) # 빨간색 LED 끔
print(＂Motion Detected !＂)
time.sleep(0.2)
if GPIO.input(sensor) == 0: #센서가 Low(0)출력 , 평소 움직임이 감지되지 않을 때
GPIO.output(led_R, 1) # 빨간색 LED 켬
GPIO.output(led_Y, 0) # 노란색 LED 끔
time.sleep(0.2)
except KeyboardInterrupt:
print("Stopped by User")
GPIO.cleanup(
import RPi.GPIO as GPIO
import time



SOL_OFF_EN = 27


GPIO.setmode(GPIO.BCM)


GPIO.setup(SOL_OFF_EN, GPIO.IN)


while True:
	if GPIO.input(SOL_OFF_EN) == False:
		print("false")
	else:
		print("true")
	time.sleep(0.5)

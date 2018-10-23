import RPi.GPIO as GPIO
import time


gpio1 = 31 
gpio2 = 33 
gpio3 = 35 

qc1 = 24
qc2 = 26

GPIO.setmode(GPIO.BOARD)

GPIO.setup(gpio1, GPIO.OUT)
GPIO.setup(gpio2, GPIO.OUT)
GPIO.setup(gpio3, GPIO.OUT)


GPIO.setup(qc1, GPIO.OUT)
GPIO.setup(qc2, GPIO.OUT)

GPIO.output(gpio1, False)
GPIO.output(gpio2, True)
GPIO.output(gpio3, False)


GPIO.output(qc1, True)
GPIO.output(qc2, False)

try:
	while True:
		time.sleep(1)	
except KeyboardInterrupt:
	GPIO.cleanup()

	print("Quit")


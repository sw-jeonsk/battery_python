import RPi.GPIO as GPIO
import time

led = 18
led2 = 23
led3 = 24
led4 = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)

GPIO.output(led, False)
GPIO.output(led2, False)
GPIO.output(led3, False)
GPIO.output(led4, False)


try:
	while True:
		

		time.sleep(1)
		GPIO.output(led2, True)
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
	print("quit")

	



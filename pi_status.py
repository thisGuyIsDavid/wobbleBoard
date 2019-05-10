import RPi.GPIO as GPIO
import time

try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(25, GPIO.IN)

	GPIO.output(23, GPIO.HIGH)
	while True:
		if not GPIO.input(25):  # if port 25 == 1
			print("Port 25 is 1/HIGH/True - LED ON")
		time.sleep(1)
except KeyboardInterrupt:
	pass
finally:
	GPIO.output(25, GPIO.LOW)
	GPIO.output(23, GPIO.LOW)
	GPIO.cleanup()
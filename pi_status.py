import RPi.GPIO as GPIO

try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
	GPIO.output(23, GPIO.HIGH)
	while True:
		pass
except KeyboardInterrupt:
	pass
finally:
	GPIO.output(23, GPIO.LOW)
	GPIO.cleanup()
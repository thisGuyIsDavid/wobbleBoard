import RPi.GPIO as GPIO
import time
import subprocess

#				subprocess.call(['shutdown', '-h', 'now'], shell=False)

try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)

	GPIO.output(23, GPIO.HIGH)
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	pass
finally:
	GPIO.output(23, GPIO.LOW)
	GPIO.cleanup()
import RPi.GPIO as GPIO
import time
from main import WobbleReader
import subprocess

#				subprocess.call(['shutdown', '-h', 'now'], shell=False)

try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
	GPIO.output(23, GPIO.HIGH)
	WobbleReader().run()
except KeyboardInterrupt:
	pass
finally:
	GPIO.output(23, GPIO.LOW)
	GPIO.cleanup()
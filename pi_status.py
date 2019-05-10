import RPi.GPIO as GPIO

#				subprocess.call(['shutdown', '-h', 'now'], shell=False)

try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
	GPIO.output(23, GPIO.HIGH)
except KeyboardInterrupt:
	pass
finally:
	GPIO.output(23, GPIO.LOW)
	GPIO.cleanup()
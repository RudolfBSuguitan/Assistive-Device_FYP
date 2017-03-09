import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

BTNSHUT=26
BTNMF=17
BTNMT=27

GPIO.setup(BTNSHUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTNMF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTNMT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

count=0
num=0
try:
	while True:
		while GPIO.input(BTNSHUT)==0:
			print "Button Shut Down"
			count+=1
			time.sleep(1)
			if count == 3:
				print "Success"
				num=1
				time.sleep(2)
				break
		count=0
		if GPIO.input(BTNMF)==0:
			print "Button Front Mode"
			time.sleep(0.1)
		if GPIO.input(BTNMT)==0:
			print "Button Three Sensors Mode"
			time.sleep(0.1)
		
		if num == 1:
			break


finally:
	print "Finish"
	GPIO.cleanup()

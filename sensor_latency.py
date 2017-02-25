import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

def usensor(trig, echo):
        GPIO.output(trig, False)

        GPIO.output(trig, True)
        time.sleep(0.00001)
	GPIO.output(trig, False)

        while GPIO.input(echo)==0:
                pulse_start = time.time()

        while GPIO.input(echo)==1:
                pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)

        return distance


TRIGFRONT = 25
ECHOFRONT = 8

while True:
        GPIO.setup(TRIGFRONT,GPIO.OUT)
        GPIO.setup(ECHOFRONT,GPIO.IN)

        distance = usensor(TRIGFRONT, ECHOFRONT)
	ws_time = time.time()
	w_time = tim.time() - ws_time
	print "While time: ", w_time
	break

        #if distance > 100:
		#s_time = time.time()
        #if distance < 100:
                #print "Checking Distance:",distance - 0.5,"cm"
		#e_time = time.time()

		#latency = e_time - s_time
		#print "Latency: ", latency
		#break



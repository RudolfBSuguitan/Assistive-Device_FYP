#measure the latency to show how fast it cen provide warnings to users
#corraborating the 3 senors to make sure they are all working together without losing performance
#measure power consumption and check if it can be more efficient without losing performance
from subprocess import call

import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

def call_reboot(trigfront, echofront):
	call_shut = 0
	while True:
		time.sleep(0.5)
		distance = usensor(trigfront, echofront)
		if distance <= 5:
			call_shut+=1
			if call_shut == 10:
				break
		if distance > 5:
			print "Cancelling Reboot"
			break
	return call_shut
	

def usensor(trig, echo):
	pulse_start=0
	pulse_end=0
        GPIO.output(trig, False)
        #print "Front"
        #time.sleep(0.05)

        GPIO.output(trig, True)
        time.sleep(0.00001)                      #Delay of 0.00001 seconds Provide trigger signal to TRIG input, it requires a HIGH signal of atleast 10us duration.
        GPIO.output(trig, False)

        while GPIO.input(echo)==0:               #Check whether the ECHO is LOW
		pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(echo)==1:               #Check whether the ECHO is HIGH
                pulse_end = time.time()                #Saves the last known time of HIGH pulse

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)            #Round to two decimal points

        return distance


def warningFront():
	pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/ObjectFront.wav")
	pygame.mixer.music.play()
	time.sleep(1.8)
	return

def curPos(warn_dist):

	#warningFront()

	distance = usensor(TRIGFRONT, ECHOFRONT)
	dist_up = warn_dist+5
	dist_down = warn_dist-5

	while True:
		if dist_up >= distance and dist_down <= distance:
			time.sleep(0.2)
			distance = usensor(TRIGFRONT, ECHOFRONT)
			print "Stationary Decrease: ", distance
		else:
			break
	

TRIGFRONT = 25
ECHOFRONT = 8

#TRIGLEFT
#ECHOLEFT

#TRIGRIGHT
#ECHORIGHT

GPIO.setup(TRIGFRONT,GPIO.OUT)
GPIO.setup(ECHOFRONT,GPIO.IN)

num_shut=0

while True:
	distance = usensor(TRIGFRONT, ECHOFRONT)
	
        if distance > 100:
                 print "Distance Front:",distance,"cm" 
        if distance <= 100 and distance > 5:
		print "Checking Distance:",distance, "cm"  
		time.sleep(0.5)

		distance = usensor(TRIGFRONT, ECHOFRONT)

		if distance <= 100 and not distance <= 5:
                	print "WARNING", distance
               		warningFront()

			warn_dist = distance
			curPos(warn_dist)
	
	if distance <= 5:
		print "Preparing to shutdown"
		time.sleep(5)
		num_shut=call_reboot(TRIGFRONT, ECHOFRONT)
		if num_shut == 10:
			print"Success"
			break
		#time.sleep(5)
		
GPIO.cleanup()
time.sleep(3)
call('reboot')



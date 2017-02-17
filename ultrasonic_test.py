import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

def usensor(trig, echo):
        GPIO.output(trig, False)
        #print "Front"
        time.sleep(0.05)

        GPIO.output(trig, True)
        time.sleep(0.00001)                      #Delay of 0.00001 seconds Provide trigger signal to TRIG input, it requires a HIGH signal of atleast 10us duration.
        GPIO.output(trig, False)

        while GPIO.input(echo)==0:               #Check whether the ECHO is LOW
                pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(echo)==1:               #Check whether the ECHO is HIGH
                pulse_end = time.time()                #Saves the last known time of HIGH pulse

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)            #Round to two decimal points

        return distance


TRIGFRONT = 25
ECHOFRONT = 8

while True:
        GPIO.setup(TRIGFRONT,GPIO.OUT)
        GPIO.setup(ECHOFRONT,GPIO.IN)

	distance = usensor(TRIGFRONT, ECHOFRONT)
	
        if distance > 80:      #Check whether the distance is within range
                print "Distance Front:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
        if distance < 80:
		print "Distance Front:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
		time.sleep(0.5)
		distance = usensor(TRIGFRONT, ECHOFRONT)
		if distance < 80:
                	print "WARNING", distance                   #display out of range
                	pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/ObjectFront.wav")
                	pygame.mixer.music.play()
                	time.sleep(2)


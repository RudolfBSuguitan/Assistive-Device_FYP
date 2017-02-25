import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

def usensor(trig, echo):
        GPIO.output(trig, False)
        #print "Front"
        #time.sleep(0.05)

        GPIO.output(trig, True)
        time.sleep(0.00001)                      #Delay of 0.00001 seconds Provide trigger signal to TRIG input, it requires a HIGH signal of atleast 
        GPIO.output(trig, False)

        while GPIO.input(echo)==0:               #Check whether the ECHO is LOW
                pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(echo)==1:               #Check whether the ECHO is HIGH
                pulse_end = time.time()                #Saves the last known time of HIGH pulse

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)            #Round to two decimal points

        return distance


def warningFront():
        pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/ObjectFront.wav")
        pygame.mixer.music.play()
	time.sleep(1.8)
        return

def curPos(warn_dist):

        warningFront()

        distance = usensor(TRIGFRONT, ECHOFRONT)
        dist_up = warn_dist+5
        dist_down = warn_dist-5

        while True:
                if dist_up >= distance and dist_down <= distance:
                        time.sleep(0.2)
                        distance = usensor(TRIGFRONT, ECHOFRONT)
                        print "Stationary Decrease: ", distance
                #elif dist_down >= distance:
                #       while True:
                #               print "Distance Increase: ", distance
		#               if dist_up < distance:
                #                       break 
                else:
                        break


TRIGFRONT = 25
ECHOFRONT = 8

while True:
        GPIO.setup(TRIGFRONT,GPIO.OUT)
        GPIO.setup(ECHOFRONT,GPIO.IN)

        distance = usensor(TRIGFRONT, ECHOFRONT)

        if distance > 100:      #Check whether the distance is within range
                print "Distance Front:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
        if distance < 100:
                print "Checking Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
		time.sleep(0.5)
                distance = usensor(TRIGFRONT, ECHOFRONT)
                if distance < 100:
                        print "WARNING", distance                   #display out of range
                        #warningFront()
                        warn_dist = distance

                        curPos(warn_dist)
                        #distance = usensor(TRIGFRONT, ECHOFRONT)

                        #if 



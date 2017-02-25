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
                else:
                        break


TRIGFRONT = 25
ECHOFRONT = 8

while True:
        GPIO.setup(TRIGFRONT,GPIO.OUT)
        GPIO.setup(ECHOFRONT,GPIO.IN)

        distance = usensor(TRIGFRONT, ECHOFRONT)

        if distance > 100:
                print "Distance Front:",distance - 0.5,"cm"
        if distance < 100:
                print "Checking Distance:",distance - 0.5,"cm"
		time.sleep(0.5)
                distance = usensor(TRIGFRONT, ECHOFRONT)
                if distance < 100:
                        print "WARNING", distance
                        warn_dist = distance

                        curPos(warn_dist)



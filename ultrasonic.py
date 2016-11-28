import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIGFRONT = 25
ECHOFRONT = 8
TRIGLEFT = 23
ECHOLEFT = 24
TRIGRIGHT = 16
ECHORIGHT = 20


pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/welcome.wav")
pygame.mixer.music.play()
time.sleep(5)
pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/beep-07.mp3")
pygame.mixer.music.play()

while True:
	GPIO.setup(TRIGFRONT,GPIO.OUT)
	GPIO.setup(ECHOFRONT,GPIO.IN)
	GPIO.setup(TRIGLEFT,GPIO.OUT)
	GPIO.setup(ECHOLEFT,GPIO.IN)
	GPIO.setup(TRIGRIGHT,GPIO.OUT)
	GPIO.setup(ECHORIGHT,GPIO.IN)

	
	GPIO.output(TRIGLEFT, False)
	print "Left"
	time.sleep(0.05)                            #Delay of 2 seconds
	GPIO.output(TRIGLEFT, True)
	time.sleep(0.00001)                      #Delay of 0.00001 seconds
	GPIO.output(TRIGLEFT, False)

	while GPIO.input(ECHOLEFT)==0:               #Check whether the ECHO is LOW
    		pulse_start = time.time()              #Saves the last known time of LOW pulse

  	while GPIO.input(ECHOLEFT)==1:               #Check whether the ECHO is HIGH
    		pulse_end = time.time()                #Saves the last known time of HIGH pulse 


  	pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  	distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  	distance = round(distance, 2)            #Round to two decimal points


  	if distance > 80:      #Check whether the distance is within range
    		print "Distance Left:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
  	else:
    		print "Left out", distance                   #display out of range
		pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/leftObject.wav")
                pygame.mixer.music.play()
		time.sleep(2)


	GPIO.output(TRIGRIGHT, False)
        print "Right"
        time.sleep(0.05)                            #Delay of 2 seconds

        GPIO.output(TRIGRIGHT, True)
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIGRIGHT, False)

        while GPIO.input(ECHORIGHT)==0:               #Check whether the ECHO is LOW
                pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(ECHORIGHT)==1:               #Check whether the ECHO is HIGH
                pulse_end = time.time()                #Saves the last known time of HIGH pulse 

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)            #Round to two decimal points


        if distance > 80:      #Check whether the distance is within range
                print "Distance RIGHT:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
        else:
                print "Right out", distance                   #display out of range
		pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/rightObject.wav")
                pygame.mixer.music.play()
		time.sleep(2)

	GPIO.output(TRIGFRONT, False)
        print "Front"
        time.sleep(0.05)

	GPIO.output(TRIGFRONT, True)
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIGFRONT, False)

        while GPIO.input(ECHOFRONT)==0:               #Check whether the ECHO is LOW
                pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(ECHOFRONT)==1:               #Check whether the ECHO is HIGH
                pulse_end = time.time()                #Saves the last known time of HIGH pulse 

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)            #Round to two decimal points


        if distance > 80:      #Check whether the distance is within range
                print "Distance Front:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
        else:
		
                print "Front out", distance                   #display out of range
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/frontObject.wav")
                pygame.mixer.music.play()
                time.sleep(2)


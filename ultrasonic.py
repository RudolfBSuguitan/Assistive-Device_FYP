import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIGLEFT = 23                                  #Associate pin 23 to TRIG
ECHOLEFT = 24

print "Distance measurement in progress"

GPIO.setup(TRIGLEFT,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHOLEFT,GPIO.IN)                   #Set pin as GPIO in

while True:
	GPIO.output(TRIGLEFT, False)
  	print "Waitng For SensorS"
  	time.sleep(1)                            #Delay of 2 seconds


  	GPIO.output(TRIGLEFT, True)
  	time.sleep(0.001)                      #Delay of 0.00001 seconds
  	GPIO.output(TRIGLEFT, False)

  	while GPIO.input(ECHOLEFT)==0:               #Check whether the ECHO is LOW
    		pulse_start = time.time()              #Saves the last known time of LOW pulse

  	while GPIO.input(ECHOLEFT)==1:               #Check whether the ECHO is HIGH
    		pulse_end = time.time()                #Saves the last known time of HIGH pulse 


  	pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  	distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  	distance = round(distance, 2)            #Round to two decimal points


  	if distance > 30:      #Check whether the distance is within range
    		print "Distance Left:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
		pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/beep-07.mp3")
		pygame.mixer.music.play()
  	else:
    		print "Out Of Range "                   #display out of range
		pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/beep-01a.mp3")
                pygame.mixer.music.play()



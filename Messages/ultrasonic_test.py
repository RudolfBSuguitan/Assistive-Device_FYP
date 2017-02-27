#corraborating the 3 senors to make sure they are all working together without losing performance
#measure power consumption and check if it can be more efficient without losing performance
#measure accuracy of sensors
#perform test

#using other python file to play sounds

from subprocess import call

import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library

GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering


ReferenceTrig = [25, 16, 23]
ReferenceEcho = [8, 20, 24]
ReferenceSensor = ["Front", "Right", "Left"]
num_shut=0

class Pin:
        def __init__(self):
                self.trig = 0
                self.echo = 0
		self.sensor = 0
#define class instances (3 objects)
pin= [Pin() for i in range(3)]


def Setup():
	for i in range(1):
		pin[i].trig = ReferenceTrig[i]  
		pin[i].echo = ReferenceEcho[i]
		pin[i].sensor = ReferenceSensor[i]

		GPIO.setup(pin[i].trig,GPIO.OUT)
		GPIO.setup(pin[i].echo,GPIO.IN)

		print "--Setup--"
		print "Sensor: ", pin[i].sensor, " Trigger: ", pin[i].trig, " Echo: ", pin[i].echo
		time.sleep(3) 
	 

def call_reboot(trig, echo):
	call_shut = 0
	while True:
		time.sleep(0.5)
		distance = usensor(trig, echo)
		print "Distance from Reboot Function", distance
		if distance <= 5 and distance > 2:
			call_shut+=1
			if call_shut == 10:
				print "Starting Reboot"
				break
		if distance > 5:
			print "Cancelling Reboot"
			time.sleep(1.8)
			break
	return call_shut
	

def usensor(trig, echo):
	pulse_start=0
	pulse_end=0

        GPIO.output(trig, False)
	#optimal speed before errors occured
        GPIO.output(trig, True)
	time.sleep(0.02)                      #Delay of 0.00001 seconds Provide trigger signal to TRIG input, it requires a HIGH signal of atleast 10us duration.
        GPIO.output(trig, False)


        while GPIO.input(echo)==0:               #Check whether the ECHO is LOW
		pulse_start = time.time()              #Saves the last known time of LOW pulse
		
	while GPIO.input(echo)==1:               #Check whether the ECHO is HIGH
		 pulse_end = time.time()                #Saves the last known time of HIGH pulse


        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)

        return distance


def warningMessage(sensor):
	if sensor == "Front":
		pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/ObjectFront.wav")
	elif sensor == "Right":
		pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/ObjectFront.wav")
	elif sensor == "Left":
		pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/ObjectFront.wav")
	pygame.mixer.music.play()
	time.sleep(1.8)

	return

def curPos(warn_dist, trig, echo):
	distance = usensor(trig, echo)
	dist_up = warn_dist+10
	dist_down = warn_dist-10

	warning=0
	num_shut=0

	while True:
		time.sleep(0.2)
		distance = usensor(trig, echo)
		if dist_up >= distance and dist_down <= distance:
			print "Stationary Distance: ", distance
		elif distance > dist_up and distance > 10:
			time.sleep(0.2)
			distance = usensor(trig, echo)
			if distance > dist_up:
				warning=0
				break
		elif dist_down > distance and distance > 10:
			time.sleep(0.2)
                        distance = usensor(trig, echo)
			if dist_down > distance:
				warning=1
				break
		elif distance <= 10 and distance > 2:
			time.sleep(0.5)
                        distance = usensor(pin[i].trig, pin[i].echo)
                        if distance <= 5 and distance > 2:
                                print "SSSPreparing to Reboot. Distance is: ", distance
                                warning=2
				break
	return warning

detection_range=100

#MAIN
Setup()

stack = [0,0,0,0]
stackSize = 8 # for starters buffer .18 miliseconds delay

#buffer delay + system delay + audio delay = total delay
while True:
	readIn = usensor(pin[0].trig, pin[0].echo) # Grab Raw
	stack.append(readIn)
	if len(stack) > stackSize:
		stack.pop(0)
	
	#print stack
	strout = readIn,  " vs ",  round((sum(stack)/len(stack)),2)
	print strout, time.time()
	

while True:
	for i in range(1):
		distance = usensor(pin[i].trig, pin[i].echo)
	
        	if distance > detection_range:
			print "Distance: ",pin[i].sensor, distance,"cm"
 
        	elif distance <= detection_range and distance > 30 :
			print "Checking Distance:", distance, "cm"  
			temp_distance = distance
			distance = usensor(pin[i].trig, pin[i].echo)
			
			if distance > temp_distance:
				print "Bad Reading", distance
				time.sleep(1)
				break

			elif distance <= detection_range and distance > 20:
				warning = curPos(distance, pin[i].trig, pin[i].echo) 
				if warning == 1:
					print "WARNING", usensor(pin[i].trig, pin[i].echo)
                                	warningMessage(pin[i].sensor)
				elif warning == 0:
			 		print "Object Moving Forward"
				elif warning == 2:
					print "Rebooting"
					break
				
		elif distance <= 20 and distance > 10:
			print "Area of No Detection: ", distance
	
		elif distance <= 10 and distance > 2:
			time.sleep(0.5)
			distance = usensor(pin[i].trig, pin[i].echo)
			if distance <= 5 and distance > 2:
				print "Preparing to Reboot. Distance is: ", distance
				time.sleep(1.8)
				num_shut=call_reboot(pin[i].trig, pin[i].echo)
			
				if num_shut == 10:
					print"Success"
					break
				else:
					num_shut=0
			else:
				break

		#elif distance < 2 and distance > 400:
			#print "Out of bounce distance: ", distance

	if num_shut == 10:
		break
		
GPIO.cleanup()
time.sleep(3)
print "END"
#call('reboot')



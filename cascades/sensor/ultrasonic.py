#corraborating the 3 senors to make sure they are all working together without losing performance
#measure power consumption and check if it can be more efficient without losing performance
#measure accuracy of sensors
#perform test

#using other python file to play sounds

from subprocess import call
from Warnings import warningMessage
from Warnings import n_warning

import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#recommended delay of 60ms 
p_cycle=0.02	#able to optimize down to 20ms

#the higher the stack size the less noises and more stable reading.
stackF = []
stackR = []
stackL = []
#size 8 for starters buffer 124  miliseconds delay
stackSize=8

detection_range=200

ReferenceTrig = [25, 16, 23]
ReferenceEcho = [8, 20, 24]
ReferenceSensor = ["Front", "Right", "Left"]

class Pin:
        def __init__(self):
                self.trig = 0
                self.echo = 0
		self.sensor = 0
#define class instances (3 objects)
pin= [Pin() for i in range(3)]


def Setup():
	for i in range(3):
		pin[i].trig = ReferenceTrig[i]  
		pin[i].echo = ReferenceEcho[i]
		pin[i].sensor = ReferenceSensor[i]

		GPIO.setup(pin[i].trig,GPIO.OUT)
		GPIO.setup(pin[i].echo,GPIO.IN)

		print "--Setup--"
		print "Sensor: ", pin[i].sensor, " Trigger: ", pin[i].trig, " Echo: ", pin[i].echo
		time.sleep(1) 
	 

def call_reboot(trig, echo):
	call_shut = 0
	while True:
		time.sleep(0.2)
		distance = usensor(trig, echo)
		print "Distance from Reboot Function", distance
		if distance <= 5 and distance > 2:
			call_shut+=1
			if call_shut == 10:
				print "Starting Reboot"
				break
		if distance > 5:
			print "Cancelling Reboot"
			time.sleep(0.3)
			break
	return call_shut
	

def usensor(trig, echo):
	pulse_start=0
	pulse_end=0
        GPIO.output(trig, False)
	#optimal speed before errors occured
        time.sleep(p_cycle)
	GPIO.output(trig, True)
	time.sleep(0.00001)                      #Delay of 0.02 seconds Provide trigger signal to TRIG input, it requires a HIGH signal of atleast 10us duration.
        GPIO.output(trig, False)


        while GPIO.input(echo)==0:               #Check whether the ECHO is LOW
		pulse_start = time.time()              #Saves the last known time of LOW pulse
		
	while GPIO.input(echo)==1:               #Check whether the ECHO is HIGH
		 pulse_end = time.time()                #Saves the last known time of HIGH pulse


        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 1)

        return distance

def curPos(warn_dist, trig, echo, sensor):
	distance = dist_avg(trig, echo, sensor)
	#increases sensitivity as object get closer to user
	#the average distance a warning should be provided to the user is 1.8 m
	#detection at 200 which calculates to 10percent threshold
	dist_allowance = (distance*0.20)
	dist_up = distance + dist_allowance
	dist_down = distance - dist_allowance

	warning=5

	while True:
		distance = dist_avg(trig, echo, sensor)
		#if dist_up >= distance and dist_down <= distance:
			#print "Stationary Distance: ", distance
		if distance > dist_up and distance > 10:
			#distance = dist_avg(trig, echo)
			#if distance > dist_up and distance > 10:
			warning=0
			break
		elif dist_down > distance and distance > 10:
                        #distance = dist_avg(trig, echo)
			#if dist_down > distance and distance > 10:
			warning=1
			break
		elif distance <= 10 and distance > 2:
                        distance = dist_avg(trig, echo, sensor)
                        if distance <= 5 and distance > 2:
                                print "SSSPreparing to Reboot. Distance is: ", distance
                                warning=2
				break
	return warning
	
def dist_avg(trig, echo, sensor):
	readIn = usensor(trig, echo) # Grab Raw
	if sensor == "Front":
		stackF.append(readIn)
		if len(stackF) > stackSize:
			stackF.pop(0)

		#strout = readIn,  " vs ",  round((sum(stackF)/len(stackF)),1)
		#calculating the speed of buffer
		#print strout, time.time()

		distance = round((sum(stackF)/len(stackF)),1)

	elif sensor == "Right":
                stackR.append(readIn)
                if len(stackR) > stackSize:
                        stackR.pop(0)

                distance = round((sum(stackR)/len(stackR)),1)

	elif sensor == "Left":
                stackL.append(readIn)
                if len(stackL) > stackSize:
                        stackL.pop(0)

                distance = round((sum(stackL)/len(stackL)),1)

	return distance

#testing the accuracy and speed
#s_time=time.time()
#readings=0
#distance_avg=0

def c_mode():
	num_shut=0
	while True:
		for i in range(3):
			#1 min tests then 5 min tests
			#measuring the approximate time to sample in the data
			distance = dist_avg(pin[i].trig, pin[i].echo, pin[i].sensor)
 			#readings+=1
			#distance_avg+=distance
		
        		if distance <= detection_range and distance > 20 :
				#print "Checking Distance:", distance, "cm"  
		
				warning = curPos(distance, pin[i].trig, pin[i].echo, pin[i].sensor) 
			
				if warning == 1:
					#print "WARNING", dist_avg(pin[i].trig, pin[i].echo)
                                	warningMessage(pin[i].sensor)
				#elif warning == 0:
			 	#print "Object Moving Forward"
				elif warning == 2:
					print "Rebooting"
					break
				
			if distance <= 20 and distance > 10:
				print "Area of No Detection: ", distance
	
			if distance <= 10 and distance > 2:
				#time.sleep(0.5)
				distance = dist_avg(pin[i].trig, pin[i].echo, pin[i].sensor)
				if distance <= 5 and distance > 2:
					print "Preparing to Reboot. Distance is: ", distance
					time.sleep(1.8)
					num_shut=call_reboot(pin[i].trig, pin[i].echo, pin[i].sensor)
			
					if num_shut == 10:
						print"Success"
						break
					else:
						num_shut=0
				else:
					break
		if num_shut == 10:
			break
	
		#time to get the data or to sample in the code
		#if (time.time()-s_time) > 300:
			#print "reading", readings," ", (time.time() - s_time)
			#print "Average distance: ", round((distance_avg/readings),2)
			#print "Average reading: ", (readings/5)
			#break

	return

def n_mode():
	num_shut=0
	while True:
		for i in range(3):
                        distance = dist_avg(pin[i].trig, pin[i].echo, pin[i].sensor)

                        if distance <= detection_range and distance > 20:
                                n_warning(distance, pin[i].trig, pin[i].echo, pin[i].sensor)

                        if distance <= 20 and distance > 10:
                                print "Area of No Detection: ", distance

                        if distance <= 10 and distance > 2:
                                distance = dist_avg(pin[i].trig, pin[i].echo, pin[i].sensor)
                                if distance <= 5 and distance > 2:
                                        print "Preparing to Reboot. Distance is: ", distance
                                        time.sleep(1.8)
                                        num_shut=call_reboot(pin[i].trig, pin[i].echo, pin[i].sensor)

                                        if num_shut == 10:
                                                print"Success"
                                                break
                                        else:
                                                num_shut=0
                                else:
                                        break

		if num_shut == 10:
                        break
        return

Setup()
mode_num=0
#while True:
c_mode()
#n_mode()
 	
GPIO.cleanup()
time.sleep(1)
pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/beep-01a.mp3")
pygame.mixer.music.play()
time.sleep(0.2)
#call('reboot')



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

#size 8 for starters buffer 124  miliseconds delay
stackSize=8

detection_range=150

#the higher the stack size the less noises and more stable reading.
stackF = []
stackR = []
stackL = []

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

#for the buttons - changing mode or shutting down
BTNSHUT=26 #Far Right
BTNMF=17 #Left
BTNMT=27 #Right
GPIO.setup(BTNSHUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTNMF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTNMT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def Setup():
	for i in range(3):
		pin[i].trig = ReferenceTrig[i]  
		pin[i].echo = ReferenceEcho[i]
		pin[i].sensor = ReferenceSensor[i]

		GPIO.setup(pin[i].trig,GPIO.OUT)
		GPIO.setup(pin[i].echo,GPIO.IN)

		print "--Setup--"
		print "Sensor: ", pin[i].sensor, " Trigger: ", pin[i].trig, " Echo: ", pin[i].echo
		time.sleep(0.5) 	

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

def curPos(trig, echo, sensor):
	distance = dist_avg(trig, echo, sensor)
	#increases sensitivity as object get closer to user
	#the average distance a warning should be provided to the user is 1.8 m
	#detection at 200 which calculates to 10percent threshold
	dist_allowance = (distance*0.15)
	dist_up = distance + dist_allowance
	dist_down = distance - dist_allowance

	warning=0

	while True:
		if dist_up >= distance and dist_down <= distance:
			print "Stationary Distance: ", distance
		if distance > dist_up and distance > 10:
			warning=0
			break
		elif dist_down > distance and distance > 10:
			warning=1
			print "Warning: ", distance
			break
		elif distance <= 10 and distance > 2:
                        distance = dist_avg(trig, echo, sensor)
                        if distance <= 5 and distance > 2:
                                print "SSSPreparing to Reboot. Distance is: ", distance
                                warning=2
				break
		distance = dist_avg(trig, echo, sensor)
	return warning
	
#think about reinitializing the stack arrays

def dist_avg(trig, echo, sensor):
	readIn = usensor(trig, echo) # Grab Raw
	if sensor == "Front":
		stackF.append(readIn)
		if len(stackF) > stackSize:
			stackF.pop(0)
			#del stackF[0]
		#strout = readIn,  " vs ",  round((sum(stackF)/len(stackF)),1)
		#calculating the speed of buffer
		#print strout, time.time()

		distance = round((sum(stackF)/len(stackF)),1)
		print "Front", distance
		#time.sleep(0.5)

	elif sensor == "Right":
                stackR.append(readIn)
                if len(stackR) > stackSize:
                        stackR.pop(0)
			#del stackR[0]
                distance = round((sum(stackR)/len(stackR)),1)
		print "Right", distance
		#time.sleep(0.5)		

	elif sensor == "Left":
                stackL.append(readIn)
                if len(stackL) > stackSize:
                        stackL.pop(0)
			#del stackL[0]
                distance = round((sum(stackL)/len(stackL)),1)
		print "Left", distance
		#time.sleep(0.5)

	return distance


def call_mode(m_num):
	btn_num=0
	btn_shut_cnt=0
	while GPIO.input(BTNSHUT)==0:
		print "Button Shutdown"
		btn_shut_cnt+=1
		time.sleep(1)

		if btn_shut_cnt == 3:
			print "Success"
			btn_num=10
			time.sleep(2)
			break
		if btn_shut_cnt < 3 and GPIO.input(BTNSHUT)==1:
			print "Cancelling"
			time.sleep(2)
			btn_num=m_num

	#if m_num == 3:
		#btn_front_cnt=0
		#while GPIO.input(BTNMF)==0:
			#print "Button Front Mode"
			#btn_front_cnt+=1
			#time.sleep(1)
			#if btn_front_cnt == 3:
				#print "Success"
				#btn_num=1
		#btn_front_cnt=0

	btn_mode_cnt=0
	while GPIO.input(BTNMF)==0:
		print "Changing Mode..."
		btn_mode_cnt+=1
		time.sleep(1)

		if btn_mode_cnt == 3:
			if m_num == 3:
				print "Changing to Front Mode..."
				btn_num=11
				time.sleep(2)
				break
			elif m_num == 1:
				print "Changing to Three Mode..."
				btn_num=22
				time.sleep(2)
				break
			break
		if btn_mode_cnt < 3 and GPIO.input(BTNMF)==1:
			print "Cancelling"
			time.sleep(2)
			btn_num=m_num	

	return btn_num

#testing the accuracy and speed
#s_time=time.time()
#readings=0
#distance_avg=0

def c_mode(mode):
	num_shut=0
	mode_num=0
	ret_mode_num=0
	while True:
		#1 min tests then 5 min tests
		#measuring  the approximate time to sample in the data
		#readings+=1
		#distance_avg+=distance
		distancex=150
		
		for x in range(mode):
			distance = dist_avg(pin[x].trig, pin[x].echo, pin[x].sensor)
			print "Sensor test: ", distance
			if distance <= distancex:
				distancex = distance
				i=x
		
		if distancex < detection_range and distancex > 10 : 
			print "Checking"		
			warning = curPos(pin[i].trig, pin[i].echo, pin[i].sensor) 
			
			if warning == 1:
				#print "WARNING", dist_avg(pin[i].trig, pin[i].echo, pin[i].sensor)
                                warningMessage(pin[i].sensor)
			elif warning == 0:
				print "Object Moving Forward"
			elif warning == 2:
				print "Rebooting"
				
		#elif distance <= 20 and distance > 10:
			#print "Area of No Detection: ", distance
	


		if GPIO.input(BTNSHUT)==0:
                        print "Button Shutdown.."
			mode_num=call_mode(mode)

                if GPIO.input(BTNMF)==0:
                        print "Button Mode Changer"
			mode_num=call_mode(mode)

                if GPIO.input(BTNMT)==0:
                        print "Button Panic Mode"
			call_mode(mode)

		if mode_num == 10 or mode_num == 11 or mode_num == 22:
			break
	
		#time to get the data or to sample in the code
		#if (time.time()-s_time) > 300:
			#print "reading", readings," ", (time.time() - s_time)
			#print "Average distance: ", round((distance_avg/readings),2)
			#print "Average reading: ", (readings/5)
			#break

	return mode_num

Setup()
front_mode=1
three_mode=3
det_mode=3
num_mode=0

#Think about changing the buffer size and delay time
while True:
	if num_mode==11:
		print "Front Mode"
		stackF=[]
		stackR=[]
		stackL=[]
		num_mode=c_mode(front_mode)
	elif num_mode==22:
		print "Three Mode"
		stackF=[]
		stackR=[]
		stackL=[]
		num_mode=c_mode(three_mode)
	elif num_mode==33:
		print "Changing to Distance Mode"
		break
		num_mode=d_mode(det_mode)
	elif num_mode==10:
		print "Rebooting"
		break
	elif num_mode==0:
		print "Default Front Mode"
		time.sleep(2)
		num_mode=c_mode(front_mode)	



GPIO.cleanup()
time.sleep(1)
#pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/beep-01a.mp3")
#pygame.mixer.music.play()
print "Finish"
#call('reboot')



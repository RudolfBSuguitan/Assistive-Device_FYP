from subprocess import call

from Warnings import warn_msg
from Distance import dist_avg
from Distance import cur_pos

import time
import threading

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

detection_range=150

send_msg_temp=0

exitFlag=0

ReferenceTrig = [25, 16, 23]
ReferenceEcho = [8, 20, 24]
ReferenceSensor = ["Front", "Right", "Left"]

ReferencePin = [26, 17, 27]
ReferenceButton = ["Shutdown", "Mode", "Panic"]

LOOP=True

sf_distance=0
sr_distance=0
sl_distance=0

class Sensor:
	def __init__(self):
		self.trig = 0
		self.echo = 0
		self.sensor = 0
#define class instances (3 objects)
pin= [Sensor() for i in range(3)]

class Button:
	def __init__(self):
		self.pin = 0
		self.button = 0
btn=[Button() for i in range(3)]

def setup():
	for i in range(3):
		pin[i].trig = ReferenceTrig[i]  
		pin[i].echo = ReferenceEcho[i]
		pin[i].sensor = ReferenceSensor[i]

		btn[i].pin = ReferencePin[i]
		btn[i].button = ReferenceButton[i]

		GPIO.setup(pin[i].trig,GPIO.OUT)
		GPIO.setup(pin[i].echo,GPIO.IN)

		GPIO.setup(btn[i].pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		print "--Setup--"
		print "Sensor: ", pin[i].sensor, ". Trigger: ", pin[i].trig, ". Echo: ", pin[i].echo
		print "Button: ", btn[i].button, ". Pin: ", btn[i].pin
		time.sleep(0.5)

def call_mode(m_num, bpin, btn):
	btn_num=0
	count=0
	while GPIO.input(bpin)==0:
		print "Button: ", btn
		count+=1
		time.sleep(1)

		if count == 3:
			print "Success"
			if btn == "Shutdown":
				global LOOP
                        	LOOP=False

				print "Rebooting"
				btn_num=10
				time.sleep(2)
				break
			elif btn == "Mode":
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

		if count < 3 and GPIO.input(bpin)==1:
			print "Cancelling"
			time.sleep(2)
			btn_num=m_num
	return btn_num

def runThread(trig, echo, sensor):
	global LOOP
	global sf_distance
	global sr_distance
	global sl_distance

	while LOOP:
		if sensor == 'Front':
			#s_time = time.clock()
			sf_distance = dist_avg(trig, echo, sensor)
			#print time.clock() - s_time
		elif sensor == 'Right':
			sr_distance = dist_avg(trig, echo, sensor)
		elif sensor == 'Left':
			s1_distance = dist_avg(trig, echo, sensor)

def startThread(mode):
	if mode == 1:
		s1T = threading.Thread(target=runThread, args=(pin[0].trig, pin[0].echo, pin[0].sensor))
		print "Starting Thread"
		time.sleep(2)
		s1T.start()
		print "Stopping Thread"
		time.sleep(2)
	elif mode == 3:
		s1T = threading.Thread(target=runThread, args=(pin[0].trig, pin[0].echo, pin[0].sensor))
		s2T = threading.Thread(target=runThread, args=(pin[1].trig, pin[1].echo, pin[1].sensor))
		s3T = threading.Thread(target=runThread, args=(pin[2].trig, pin[2].echo, pin[2].sensor))

		s1T.start()
		s2T.start()
		s3T.start()

def c_mode(mode):
	mode_num=0
	startThread(mode)
	while True:

		for i in range(3):
                        if GPIO.input(btn[i].pin)==0:
				print "Button pressed..."
				mode_num=call_mode(mode, btn[i].pin, btn[i].button)
				break

		if mode_num == 10 or mode_num == 11 or mode_num == 22:
			break

	return mode_num

def main():
	front_mode=1
	three_mode=3
	num_mode=0
	num=1

	while True:
		if num_mode==11:
			print "Front Mode"
			num_mode=c_mode(front_mode)
		elif num_mode==22:
			print "Three Mode"
			num_mode=c_mode(three_mode)
		elif num_mode==10:
			print "Rebooting"
			global LOOP
			LOOP=False
			time.sleep(2)
			break
		elif num_mode==0:
			print "Default Front Mode"
			time.sleep(2)
			num_mode=c_mode(front_mode)	

if __name__ == "__main__":
	setup()
	main()
	GPIO.cleanup()
	time.sleep(1)
	print "Finish"
	#call('reboot')



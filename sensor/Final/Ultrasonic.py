from subprocess import call

from Warnings import warn_msg
from Distance import dist_avg
from Distance import cur_pos

import time

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
			elif btn == "Panic":
				print "Sending Message"
				btn_num=30
				time.sleep(2)
				break

		if count < 3 and GPIO.input(bpin)==1:
			print "Cancelling"
			time.sleep(2)
			btn_num=m_num
	return btn_num

def c_mode(mode):
	mode_num=0
	while True:
		distancex=150

		s_time = time.clock()
		for x in range(mode):
			start=time.clock()
			#print time.clock()-start
			distance = dist_avg(pin[x].trig, pin[x].echo, pin[x].sensor)
			print time.clock()-start
			if distance <= distancex:
				distancex = distance
				i=x
		print "Time delay: ", time.clock()-s_time
		
		if distancex < detection_range and distancex > 10 : 
			print "Checking"		
			warning = cur_pos(pin[i].trig, pin[i].echo, pin[i].sensor) 
			
			if warning == 1:
                                warn_msg(pin[i].sensor)
			elif warning == 0:
				print "Object Moving Forward"

		for i in range(3):
                        if GPIO.input(btn[i].pin)==0:
				print "Button pressed..."
				mode_num=call_mode(mode, btn[i].pin, btn[i].button)
				break

		if mode_num == 10 or mode_num == 11 or mode_num == 22:
			break

		elif mode_num == 30:
			global send_msg_temp
			if mode == 1:
				send_msg_temp=11
			elif mode == 3:
				send_msg_temp=22
			break

	return mode_num

#Think about changing the buffer size and delay time
#While True then false the other scripts
#create a class each
def main():
	front_mode=1
	three_mode=3
	num_mode=0

	while True:
		if num_mode==11:
			print "Front Mode"
			num_mode=c_mode(front_mode)
		elif num_mode==22:
			print "Three Mode"
			num_mode=c_mode(three_mode)
		elif num_mode==33:
			print "Changing to Distance Mode"
			break
			num_mode=d_mode(three_mode)
		elif num_mode==10:
			print "Rebooting"
			break
		elif num_mode==30:
			print "Sending Message"
			call('./runScript.sh')
			num_mode=send_msg_temp
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



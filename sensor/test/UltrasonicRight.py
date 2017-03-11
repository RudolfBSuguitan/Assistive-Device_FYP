from Warnings import warn_msg
from Distance import dist_avg
from Distance import cur_pos

import os
#####################global variable from other scipts to access values and stop the process

import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

detection_range=150

ReferenceTrig = [16, 23, 25]
ReferenceEcho = [20, 24, 8]
ReferenceSensor = ["Right", "Left", "Front"]

spid=os.getpid()

class Sensor:
        def __init__(self):
                self.trig = 0
                self.echo = 0
		self.sensor = 0
#define class instances (3 objects)
pin= [Sensor() for i in range(3)]

def setup():
	for i in range(1):
		pin[i].trig = ReferenceTrig[i]  
		pin[i].echo = ReferenceEcho[i]
		pin[i].sensor = ReferenceSensor[i]

		GPIO.setup(pin[i].trig,GPIO.OUT)
		GPIO.setup(pin[i].echo,GPIO.IN)

		print "--Setup--"
		print "Sensor: ", pin[i].sensor, ". Trigger: ", pin[i].trig, ". Echo: ", pin[i].echo
		time.sleep(0.5)

def c_mode():
	while True:
		start=time.clock()
		distance = dist_avg(pin[0].trig, pin[0].echo, pin[0].sensor)
		print spid, " - ", time.clock()-start
		
		if distance < detection_range and distance > 10 : 
			print "Checking"		
			warning = cur_pos(pin[0].trig, pin[0].echo, pin[0].sensor) 
			
			if warning == 1:
                                warn_msg(pin[0].sensor)
			elif warning == 0:
				print "Object Moving Forward"

	return

#Think about changing the buffer size and delay time
#While True then false the other scripts
#create a class each
def main():
	c_mode()	

if __name__ == "__main__":
	setup()
	main()



from subprocess import call

from Warnings import warn_msg
from Warnings import respMessage
from Warnings import warnCam
from Distance import dist_avg
from Distance import cur_pos

from timeit import default_timer as timer
import time
import numpy as np
import cv2
import threading


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

detection_range=100

dBus = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/dbus.xml')
cleanSign = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/CleaningSign.xml')
pedBtn = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/pedButton.xml')
TrafL = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/TrafficL2.xml')
stop2 = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/Stop2.xml')

send_msg_temp=0
send_msg_temp2=0

LOOP=False

ReferenceTrig = [25, 16, 23]
ReferenceEcho = [8, 20, 24]
ReferenceSensor = ["Front", "Right", "Left"]

ReferencePin = [26, 17, 27, 19]
ReferenceButton = ["Shutdown", "Mode", "Panic", "PiCam"]

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
btn=[Button() for i in range(4)] 

def setup():
	for i in range(3):
		pin[i].trig = ReferenceTrig[i]  
		pin[i].echo = ReferenceEcho[i]
		pin[i].sensor = ReferenceSensor[i]

		GPIO.setup(pin[i].trig,GPIO.OUT)
		GPIO.setup(pin[i].echo,GPIO.IN)

		print "--Setup--"
		print "Sensor: ", pin[i].sensor, ". Trigger: ", pin[i].trig, ". Echo: ", pin[i].echo
		time.sleep(0.5)
	
	for x in range(4):
                btn[x].pin = ReferencePin[x]
                btn[x].button = ReferenceButton[x]

                GPIO.setup(btn[x].pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

                print "Button: ", btn[x].button, ". Pin: ", btn[x].pin
                time.sleep(0.5)
	return

def itemPos(x, sign):
	if sign=="BusSign":
		#print sign
		pass
        elif sign=="StopSign":
		#print sign
		pass
        elif sign=="PedButton":
		#print sign
		pass
        elif sign=="CleanSign":
		#print sign
		pass
        elif sign=="PedLight":
		#print sign
		pass

        if x <= 150 and x >= 1:
                #print "Left Object"
		loc="Left"
        elif x > 150 and x <= 395:
                #print "Centre Object"
		loc="Front"
        elif x > 395:
                #print "Right Object"
		loc="Right"

	#warnCam(loc, sign)
        return

def camThread():
        video = cv2.VideoCapture(0)
        time.sleep(3)
	BS="BusSign"
	SS="StopSign"
	PB="PedButton"
	CS="CleanSign"
	PL="PedLight"
	
        global LOOP
	s_time=time.time()
	count=0
        while True:
		if LOOP == True:
                	ret, OriginalFrame = video.read()
			count+=1
                	gray = cv2.cvtColor(OriginalFrame, cv2.COLOR_BGR2GRAY)

                	#ped = pedBtn.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(40, 40), maxSize=(90,90))
                	#traf = TrafL.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=3, minSize=(60, 60), maxSize=(80, 80))
                	#cSign = cleanSign.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=3, minSize=(65, 65), maxSize=(90,90))
                	#stopSign = stop2.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60), maxSize=(80, 80))
                	#Bus = dBus.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(55, 55), maxSize=(75, 75))

			ped = pedBtn.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=6, minSize=(45, 45), maxSize=(82,82))
			traf = TrafL.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=3, minSize=(60, 60), maxSize=(150, 150))
			cSign = cleanSign.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=4, minSize=(73, 73), maxSize=(99,99))
			stopSign = stop2.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=6, minSize=(55, 55), maxSize=(97, 97))
			Bus = dBus.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=6, minSize=(55, 55), maxSize=(97, 97))

                	for (x,y,w,h) in Bus:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Bus Stop', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print BS, Bus
                        	#itemPos(x, BS)

                	#for (x,y,w,h) in traf:
                        	#cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	#font = cv2.FONT_HERSHEY_SIMPLEX
                        	#cv2.putText(OriginalFrame, 'TrafficLight', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print PL
                        	#itemPos(x, PL)

			for (x,y,w,h) in ped:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Button', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print PB, ped
                        	#itemPos(x, PB)

                	for (x,y,w,h) in stopSign:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Stop', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print SS, stopSign
                        	#itemPos(x, SS)

                	for (x,y,w,h) in cSign:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Clean', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print CS, cSign
                        	#itemPos(x, CS)

			#cv2.imshow("Main Frame", OriginalFrame)
			print time.time()-s_time
			print count

			k = cv2.waitKey(1) & 0xFF
                	if k == 27:
				LOOP=False
                        	break

		elif LOOP == False:
			time.sleep(2)
        		video.release()
        		cv2.destroyAllWindows()
			break
	return

def startThread():
	global LOOP
	global send_msg_temp2
	send_msg_temp2=0
	print "Starting Camera"
	#respMessage("ECamera")
        LOOP=True
        print LOOP
       	time.sleep(2)
        threading.Thread(target=camThread, args=()).start()

	return


def call_mode(m_num, bpin, btn):
	btn_num=0
	count=0
	global LOOP

	if btn == "Panic":
		respMessage("Assist")
	elif btn == "Shutdown":
		respMessage("Reboot")
	elif btn == "Mode" and m_num == 1:
		respMessage(3)
	elif btn == "Mode" and m_num == 3:
		respMessage(1)
	elif btn == "PiCam" and LOOP == False:
		respMessage("ECamera")
	elif btn == "PiCam" and LOOP == True:
		respMessage("DCamera")

	while GPIO.input(bpin)==0:
		print "Button: ", btn
		count+=1
		time.sleep(1)

		if count == 3:
			respMessage("Beep")
			print "Success"
			if btn == "Shutdown":
				print "Rebooting"
				LOOP=False
				print LOOP
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
				global send_msg_temp2
				print LOOP
				if LOOP == True:
					send_msg_temp2=1
					#respMessage("DCamera")
					LOOP=False
					print LOOP
				print "Sending Message"
				btn_num=30
				time.sleep(5)
				break
			elif btn == "PiCam":
				if LOOP == False:
					startThread()
				elif LOOP == True:
					print "Disabling Camera"
					#respMessage("DCamera")
					LOOP=False
					print LOOP
					time.sleep(2)
				btn_num=m_num

		if count < 3 and GPIO.input(bpin)==1:
			respMessage("Cancel")
			print "Cancelling"
			time.sleep(2)
			btn_num=m_num
	return btn_num

def c_mode(mode):
	mode_num=0
	while True:
		distancex=100
		for x in range(mode):
			distance = dist_avg(pin[x].trig, pin[x].echo, pin[x].sensor)
			if distance <= distancex:
				distancex = distance
				i=x

		if distancex < detection_range and distancex > 10 : 
			print "Checking"		
			warning = cur_pos(pin[i].trig, pin[i].echo, pin[i].sensor) 
			
			if warning == 1:
                                warn_msg(pin[i].sensor)
			elif warning == 0:
				print "Object Moving Forward"

		for i in range(4):
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
			if send_msg_temp2 == 1:
				respMessage("ECamera")
				startThread()
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
	#call('./piReboot.sh')



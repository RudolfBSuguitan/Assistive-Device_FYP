from subprocess import call

from Warnings import warn_msg
from Warnings import respMessage
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

#cv2.namedWindow("Main Frame"", cv2.WINDOW_AUTOSIZE)
dBus = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/dbus.xml')
#const = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/Construction2.xml')
cleanSign = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/CleaningSign.xml')
#rLight = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/rLight.xml')
#noPed = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/noPed.xml')
pedBtn = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/pedButton.xml')
TrafL = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/TrafficL2.xml')
stop2 = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/Stop2.xml')

#video = cv2.VideoCapture(0)

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

def itemPos(x):
        if x <= 150:
                print "Left Object"
        elif x > 150 and x <= 395:
                print "Centre Object"
        elif x > 395:
                print "Right Object"
        return

def camThread():
        video = cv2.VideoCapture(0)
        time.sleep(3)
        global LOOP

        while True:
		if LOOP == True:
                	ret, OriginalFrame = video.read()
                	gray = cv2.cvtColor(OriginalFrame, cv2.COLOR_BGR2GRAY)

                	#signs = sign_cascade.detectMultiScale(gray, 5, 5)
                	ped = pedBtn.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(40, 40), maxSize=(90,90))
                	#traffic_light2 traf = TrafL.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(45, 45), maxSize=(60, 60))
                	traf = TrafL.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=3, minSize=(60, 60), maxSize=(80, 80))
                	cSign = cleanSign.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=3, minSize=(65, 65), maxSize=(90,90))
                	stopSign = stop2.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60), maxSize=(80, 80))
                	Bus = dBus.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(55, 55), maxSize=(75, 75))

                	print traf
                	for (x,y,w,h) in Bus:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Bus Stop', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	print "Bus Stop Detected"
                        	itemPos(x)

                	#for (x,y,w,h) in traf:
                        	#cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	#font = cv2.FONT_HERSHEY_SIMPLEX
                        	#cv2.putText(OriginalFrame, 'TrafficLight', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print "Traffic Light Detected"
                        	#itemPos(x)

			for (x,y,w,h) in ped:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Button', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	print "Button Detected"
                        	itemPos(x)

                	for (x,y,w,h) in stopSign:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Stop', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	print "Stop Sign Detected"
                        	itemPos(x)

                	for (x,y,w,h) in cSign:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Clean', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	print "Clean Sign Detected"
                        	itemPos(x)

			#cv2.imshow("Main Frame", OriginalFrame)

			k = cv2.waitKey(1) & 0xFF
                	if k == 27:
                        	break

		elif LOOP == False:
			time.sleep(2)
        		#video.release()
        		#cv2.destroyAllWindows()
			break
			
	#time.sleep(2)
        #video.release()
        #cv2.destroyAllWindows()
	return

def startThread():
	global LOOP
	global send_msg_temp2
	send_msg_temp2=0
	print "Starting Camera"
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
					LOOP=False
					print LOOP
				print "Sending Message"
				#LOOP=False
				btn_num=30
				time.sleep(5)
				break
			elif btn == "PiCam":
				if LOOP == False:
					startThread()
				elif LOOP == True:
					print "Disabling Camera"
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
		#s_time=timer()
		for x in range(mode):
			distance = dist_avg(pin[x].trig, pin[x].echo, pin[x].sensor)
			if distance <= distancex:
				distancex = distance
				i=x
		#print "Time: ", timer()-s_time
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
			if send_msg_temp2 == 1:
				print "Startinnngggggggggggggggggg"
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



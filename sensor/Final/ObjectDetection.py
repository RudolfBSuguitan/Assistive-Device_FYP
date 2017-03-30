import numpy as np
import cv2
import time
import threading

LOOP=True

#cv2.namedWindow("Main Frame"", cv2.WINDOW_AUTOSIZE)
dBus = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/dbus.xml')
#const = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/Construction2.xml')
cleanSign = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/CleaningSign.xml')
#rLight = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/rLight.xml')
#noPed = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/noPed.xml')
pedBtn = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/pedButton.xml')
TrafL = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/TrafficL2.xml')
stop2 = cv2.CascadeClassifier('/home/pi/Documents/Assistive-Device_FYP/cascades/Stop2.xml')

def itemPos(x):
        if x <= 150:
                #print "Left Object"
		pass
        elif x > 150 and x <= 395:
                #print "Centre Object"
		pass
        elif x > 395:
                #print "Right Object"
		pass
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
	count=0
	s_time=time.time()
        while True:
		if LOOP == True:		
                	ret, OriginalFrame = video.read()
			count+=1
                	gray = cv2.cvtColor(OriginalFrame, cv2.COLOR_BGR2GRAY)

                	ped = pedBtn.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=6, minSize=(45, 45), maxSize=(82,82))
                	traf = TrafL.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=3, minSize=(60, 60), maxSize=(150, 150))
                	cSign = cleanSign.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=4, minSize=(73, 73), maxSize=(99,99))
                	stopSign = stop2.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=6, minSize=(55, 55), maxSize=(97, 97))
                	Bus = dBus.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=6, minSize=(55, 55), maxSize=(97, 97))

                	#print cSign
                	for (x,y,w,h) in Bus:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Bus Stop', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print BS, Bus
                        	itemPos(x)

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
                        	itemPos(x)

                	for (x,y,w,h) in stopSign:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Stop', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print SS, stopSign
                        	itemPos(x)

                	for (x,y,w,h) in cSign:
                        	cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                        	font = cv2.FONT_HERSHEY_SIMPLEX
                        	cv2.putText(OriginalFrame, 'Clean', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        	#print CS, cSign
                        	itemPos(x)

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

camT = threading.Thread(target=camThread, args=())
camT.start()

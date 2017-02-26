import numpy as np
import cv2
import time


video = cv2.VideoCapture(0)
time.sleep(0.1)

#cv2.namedWindow("Main Frame"", cv2.WINDOW_AUTOSIZE)
#sign_cascade = cv2.CascadeClassifier('/opencv-3.1.0/data/haarcascades/traffic_light_sign.xml')
construction_cascade = cv2.CascadeClassifier('/opencv-3.1.0/data/haarcascades/construction_sign.xml')


while True:
        ret, OriginalFrame = video.read()
        gray = cv2.cvtColor(OriginalFrame, cv2.COLOR_BGR2GRAY)

        #signs = sign_cascade.detectMultiScale(gray, 5, 5)
	const = construction_cascade.detectMultiScale(gray, 5, 5)

        #for (x,y,w,h) in signs:
                #cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                #font = cv2.FONT_HERSHEY_SIMPLEX
                #cv2.putText(OriginalFrame, 'Traffic', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
	
	for (x,y,w,h) in const:
                cv2.rectangle(OriginalFrame,(x,y),(x+w,y+h),(255,255,0),2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(OriginalFrame, 'Construction', (x+w, y+h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

	cv2.imshow("Main Frame", OriginalFrame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
                break

video.release()
cv2.destroyAllWindows()


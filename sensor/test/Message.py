#Sending email with attached image

import time
from datetime import datetime
from picamera import PiCamera
from smtplib import SMTP
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

dirImg=[]
camera = PiCamera()
try:
	for x in range(2):
		camera.resolution = (1024, 768)
		camera.start_preview()
		time.sleep(3)
		camera.capture('ePhotos/Capture'+str(x)+'.jpg')
		camera.stop_preview()
		dirImg.append('ePhotos/Capture'+str(x)+'.jpg')
		print "Capture"+str(x)
except:
	print "Error capturing"

COMMASPACE =', '

f_time = datetime.now().strftime('%a %d %b @ %H:%M')

toaddr = ['rudolf.suguitan@gmail.com', 'rv_suguitan@yahoo.ie']    # redacted
me = 'C13460538@mydit.ie' # redacted
subject = 'URGENT User Needs Assistance ' + f_time

msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = me
msg['To'] = COMMASPACE.join(toaddr)
msg.preamble = "User Assistance @ " + f_time

body = "Please Check my current location"
text=MIMEText(body, 'plain')
msg.attach(text)

for file in dirImg:
	fp = open(file, 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)

try:
   	s = smtplib.SMTP('smtp.gmail.com',587)
   	s.starttls()
   	s.login(user = 'C13460538@mydit.ie',password = 'Rudy1219')
   	s.sendmail(me, toaddr, msg.as_string())
   	s.quit()

	print "Message Sent!"
	dirImg=[]
except:
   	print ("Error: unable to send email")


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
COMMASPACE =', '

f_time = datetime.now().strftime('%a %d %b @ %H:%M')

toaddr = ['rudolf.suguitan@gmail.com', 'rv_suguitan@yahoo.ie']    # redacted
me = 'C13460538@mydit.ie' # redacted
subject = 'URGENT User Needs Assistance ' + f_time
uname='C13460538@mydit.ie'
upass='Rudy1219'

msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = me
msg['To'] = COMMASPACE.join(toaddr)
msg.preamble = "User Assistance @ " + f_time

body = "Please Check my current location"
text=MIMEText(body, 'plain')
msg.attach(text)

def capture(c_num): 
	try:
		for x in range(c_num):
			camera.resolution = (1024, 768)
			camera.start_preview()
			time.sleep(3)
			camera.capture('ePhotos/Capture'+str(x)+'.jpg')
			camera.stop_preview()
			dirImg.append('ePhotos/Capture'+str(x)+'.jpg')
			print "Capture"+str(x)
		resp = 'success'
	except:
		resp = 'failure'
		print "Error capturing"
	return resp

def send_mail(u_name, u_pass):
	try:
		for file in dirImg:
			fp = open(file, 'rb')
			img = MIMEImage(fp.read())
			fp.close()
			msg.attach(img)

   		s = smtplib.SMTP('smtp.gmail.com',587)
   		s.starttls()
   		s.login(user = u_name, password = u_pass)
   		s.sendmail(me, toaddr, msg.as_string())
   		s.quit()

		resp = 'success'
		print "Message Sent!"
	except:
		resp = 'failure'
   		print ("Error: unable to send email")

	return resp

num=2
captured=capture(num)

if captured == 'success':
	print 'Images captured'
	s_mail=send_mail(uname, upass)

	if s_mail == 'success':
		print 'Mail sent successfully'
	elif s_mail == 'failure':
		print 'Unable to send mail'
elif captured == 'failure':
	print 'Unable to capture images'
dirImg=[] #reinitialize

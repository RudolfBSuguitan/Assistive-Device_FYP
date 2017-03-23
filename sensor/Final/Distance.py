import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#recommended delay of 60ms 
p_cycle=0.02	#able to optimize down to 20ms

#size 8 for starters buffer 124  miliseconds delay
stackSize=8

#the higher the stack size the less noises and more stable reading.
stackF = []
stackR = []
stackL = []

BTNSHUT=26 #Far Right
BTNMF=17 #Left
BTNMT=27 #Right
BTNCAM=19
GPIO.setup(BTNSHUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTNMF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTNMT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTNCAM, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def usensor(trig, echo):
	pulse_start=0
	pulse_end=0

        GPIO.output(trig, False)
	#optimal speed before errors occured
        time.sleep(p_cycle)

	GPIO.output(trig, True)
	time.sleep(0.00001)                      #Delay of 0.02 seconds Provide trigger signal to TRIG input, it requires a HIGH signal of atleast 10us duration.
        GPIO.output(trig, False)

	s_time=time.time()
        while GPIO.input(echo)==0:               #Check whether the ECHO is LOW
		pulse_start = time.time()              #Saves the last known time of LOW pulse
		if time.time()-s_time > 1:
                        break
		
	while GPIO.input(echo)==1:               #Check whether the ECHO is HIGH
		pulse_end = time.time()                #Saves the last known time of HIGH pulse
		if time.time()-s_time > 1:
                        break

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 1)

        return distance

def cur_pos(trig, echo, sensor):
	distance = dist_avg(trig, echo, sensor)
	dist_allowance = (distance*0.15)
	dist_up = distance + dist_allowance
	dist_down = distance - dist_allowance

	warning=0

	while True:
		distance = dist_avg(trig, echo, sensor)
		if dist_up >= distance and dist_down <= distance:
			print "Stationary Distance: ", distance
		elif distance > dist_up:
			warning=0
			break
		elif dist_down > distance:
			warning=1
			print "Warning: ", distance
			break
		
		if GPIO.input(BTNSHUT)==0 or GPIO.input(BTNMF)==0 or GPIO.input(BTNMT)==0 or GPIO.input(BTNCAM)==0:
                        print "Button pressed..."
                        break
	return warning
	

def dist_avg(trig, echo, sensor):
	global stackF
	global stackR
	global stackL
	readIn = usensor(trig, echo)
	if sensor == "Front":
		stackF.append(readIn)
		#for i in stackF:
			#print "No: ", i
		if len(stackF) > stackSize:
			stackF.pop(0)
		distance = round((sum(stackF)/len(stackF)),1)
		#print "Size:", len(stackF), " Front", distance
		print "Front", distance

	elif sensor == "Right":
                stackR.append(readIn)
                if len(stackR) > stackSize:
                        stackR.pop(0)

                distance = round((sum(stackR)/len(stackR)),1)
		print "Right", distance		

	elif sensor == "Left":
                stackL.append(readIn)
                if len(stackL) > stackSize:
                        stackL.pop(0)

                distance = round((sum(stackL)/len(stackL)),1)
		print "Left", distance

	return distance


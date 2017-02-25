import pygame
pygame.mixer.init()

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

def usensor(trig, echo):
        GPIO.output(trig, False)

        GPIO.output(trig, True)
        time.sleep(0.00001)
	GPIO.output(trig, False)

        while GPIO.input(echo)==0:
                pulse_start = time.time()

        while GPIO.input(echo)==1:
                pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)

        return distance


TRIGFRONT=25
ECHOFRONT=8
Test_Distance=100
num_test=0
total_time=0

while True:
        GPIO.setup(TRIGFRONT,GPIO.OUT)
        GPIO.setup(ECHOFRONT,GPIO.IN)

	s_time = time.time()        

	distance = usensor(TRIGFRONT, ECHOFRONT)
	
        if distance <= Test_Distance:
		e_time = time.time()

		latency = e_time - s_time
		num_test+=1
		print "Test No: ", num_test
		print "Distance: ", distance
		print "Latency: ", latency

		total_time += latency

	if num_test == 10:
		avg_latency_sec = total_time/num_test
		avg_latency_mil = avg_latency_sec*1000
		avg_latency_mic = avg_latency_sec*1000000
		
		print "Distance: =<", Test_Distance 
		print "Second -> Average Latency: ", avg_latency_sec
		print "Milliseconds -> Average Latency: ", avg_latency_mil
		print "Microseconds -> Average Latency: ", avg_latency_mic

		break

	print "Wait.."
	time.sleep(3)
	print "Ready!"

GPIO.cleanup()

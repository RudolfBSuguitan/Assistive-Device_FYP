# Assistive-Device_FYP
Developing a device that could potentially guide and assist people who are visually impaired. This is done by using sensors for detection, and other functionalities that would assist users during unfortunate scenarios.


## Draft Documentation
-using python to integrate sensors
-used a prototyping breadboard which can only fir 2 ultrasonic sensors (have to buy a new one)
-2 resistors used for each sensor to avoid the pi from being fried
-using 1 sensor was successfull, 2 sensors, unfortunately no
-successfully detecting distanced and giving warning when a particular distance is detected
-sounds were downloaded from the internet
-sound will be updated to make it more modern by using human voices?
-detection will also be calibrated to check moving objects to avoid the unnecessary warnings.
-got the 2 sensors working side by side however, like it thought i would be, is a bit delayed.
-this is due to the style of coding which is FCFS. will try and address this issues usin functions
-Though i can create 2 separate programs that will run at the same time but data handling will be an issue
-using rc.local in /etc to run script on boot
-working with warning massages - messages has to be shorter but as effective to allow user react on time
-will make it smarter using functions
-better input handling




-vncserver:1

-Problem with Raspberry Pi Resources. to slow to run the camera
	-overclocked the pi but still not powerful enough
	-especially when detecting more images
	-run on linux laptop?
-training takes hours to days
-inaccurate sensors - got around by adding delays but without affecting the user too much
-test the accuracy of camera and senors
-calculate latency - particular distances
-calculate power consumption
	-ways to reduce consumption
-installing opencv
-learning how to process images


-using different modes
	-one for collission
	-one for object inputs

-use other py to run warnings
-talk about the buffer including the delay
-the averages that can be done

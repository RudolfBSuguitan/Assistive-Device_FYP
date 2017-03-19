import pygame
pygame.mixer.init()

import time

def respMessage(process):
	ms_time=0
	if process == "Beep":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/beep-01a.mp3"
		ms_time=0.2

	elif process == 1:
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/1mode.wav"
		ms_time=1.02

	elif process == 3:
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/3mode.wav"
		ms_time=1.07

	elif process == "Cancel":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/Cancelling.wav"
		ms_time=0.650

	elif process == "CapLoct":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/CapturingLocation.wav"
		ms_time=1.21

	elif process == "DCamera":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/DCamera.wav"
		ms_time=0.915

	elif process == "ECamera":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/ECamera.wav"
		ms_time=0.750

	elif process == "ESent":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/EmailSent.wav"
		ms_time=0.790

	elif process == "Error":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/Error.wav"
		ms_time=1.580

	elif process == "LoctCaptured":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/LocationCaptured.wav"
		ms_time=1.210

	elif process == "MSent":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/MessageSent.wav"
		ms_time=0.780

	elif process == "PedButton":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/PedButton.wav"
		ms_time=1

	elif process == "Reboot" :
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/Poweroff.wav"
		ms_time=0.720

	elif process == "Assist":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/RequestAssistance.wav"
		ms_time=1.250

	elif process == "SendingMail":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/SendingEmail.wav"
		ms_time=0.910

	elif process == "SendingSMS":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/SendingMessage.wav"
		ms_time=0.990

	elif process == "Setup":
		wav_dir="/home/pi/Documents/Assistive-Device_FYP/Messages/RespAudio/SetupDevice.wav"
		ms_time=1.425

	pygame.mixer.music.load(wav_dir)
	pygame.mixer.music.play()
	time.sleep(ms_time)


#warnings for sensors
def warn_msg(sensor):
        #pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/Warning410ms.wav")
        pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/beep-01a.mp3")
        pygame.mixer.music.play()
        #time.sleep(0.415)
        time.sleep(0.2)
        if sensor == "Front":
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/Front400ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.42)
        elif sensor == "Right":
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/Right280ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.30)
        elif sensor == "Left":
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/Left460ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.48)
        return


def n_warning(dist, trig, echo, sensor):
        if sensor == "Front":
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/Front400ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.400)
        elif sensor == "Right":
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/Right280ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.280)
        elif sensor == "Left":
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/Left460ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.460)

        if dist <= 200 and dist > 150:
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/New-Audio/200-530ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.530)
        elif dist <= 150 and dist > 100:
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/New-Audio/150-960ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.960)
        elif dist <= 100 and dist > 50:
                pygame.mixer.music.load("/home/pi/Documents/Assistive-Device_FYP/Messages/New-Audio/100-590ms.wav")
                pygame.mixer.music.play()
                time.sleep(0.590)


#if __name__ == "__main__":

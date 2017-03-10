import pygame
pygame.mixer.init()

import time

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

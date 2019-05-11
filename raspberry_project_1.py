import picamera
import time
import RPi.GPIO as gpio
from gpiozero import LED
import threading
import sys

class LedThread(threading.Thread):

    def __init__(self):
        super(LedThread, self).__init__()
        self._keepgoing = True

    def run(self):
        while (self._keepgoing):
            self.ledController(whiteLED)
            self.ledController(redLED)
            self.ledController(whiteLED_2)
            self.ledController(redLED)

    def ledController(self,led):
        if self._keepgoing:
            led.on()
            time.sleep(sleepTime)
            led.off()

    def stop(self):
        self._keepgoing = False     

#Final variables
TRIG=23
ECHO=22
WHITE=18
WHITE_TWO=26
RED=19
pictureName="mPic.jpg"
sleepTime=0.2

camera=picamera.PiCamera()

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)

#Setups
gpio.setup(TRIG,gpio.OUT)
gpio.setup(ECHO,gpio.IN)
gpio.setup(18,gpio.OUT)
whiteLED=LED(WHITE)
whiteLED_2=LED(WHITE_TWO)
redLED=LED(RED)

def getDistance():
    gpio.output(TRIG,True)
    time.sleep(0.0001)
    gpio.output(TRIG,False)

    while gpio.input(ECHO)==False:
        startTime=time.time()

    while gpio.input(ECHO)==True:
        endTime=time.time()

    sig_time=endTime-startTime

    distance=sig_time*17150
    distance=round(distance,2)
    return distance

def takePicture():
    camera.capture(pictureName)

def turnOffLeds():
    whiteLED.off()
    whiteLED_2.off()
    redLED.off()

flashThread=threading.Thread(target=None)
while True:
    distance=getDistance()
    time.sleep(0.1)
    if distance >2 and distance <400:
        print('Distance: {} cm'.format(distance))
        if distance < 10:
            if not flashThread.isAlive():
                flashThread=LedThread()
                flashThread.start()
                print("Just started")
            else:
                print("Alive")
        else:
            if flashThread.isAlive():
                flashThread.stop()
                print("Stopped")
            turnOffLeds()
    else:
        print('Out of range.')
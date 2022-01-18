
import os
import ftplib
import glob
import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

ftpUser = 'pi'
ftpServer = ''
ftppasswd = 'vladtepup'
folderproiect = '/images/'
folderftp = '/home/pi/ftp/files/'
session = ftplib.FTP(ftpServer,ftpUser,ftppasswd)

def take_picture():
        os.system("libcamera-jpeg -n -t 1000 -o images/poza_{}.jpeg".format(datetime.now().strftime("%d.%m.%Y_%H:%M:%S")))

	#file = open(folderproiect,'rb')
        #file = glob.glob('images/*jpeg')
        #for image in glob.glob('images/*.jpeg'):
           # with open(image, 'rb') as file:
                # session.storbinary('STOR ' + folderftp , file)
        #imageName = max(file, key = os.path.getctime)
        #session.storbinary('STOR' + folderftp,imageName)
        #file.close()
        os.system("mv images/*.jpeg {}".format(folderftp))

def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print(dist)
            if dist < 100:
                take_picture()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
       	session.close()


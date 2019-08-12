#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
import webbrowser
import os
import sqlite3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Doorlock relay
GPIO.setup(17,GPIO.OUT)

Name = ""
def sendData ():
	global Name
	#RealName = str(Name)
	THINGSBOARD_HOST = 'demo.thingsboard.io'
	ACCESS_TOKEN = 'FTCnfMcOm5CH1FhlymKE'
	sensor_data = {}
	client = mqtt.Client()
	client.username_pw_set(ACCESS_TOKEN)
	client.connect(THINGSBOARD_HOST, 1883, 60)
	client.loop_start()	
	
	sensor_data['Name'] = Name
	sensor_data['ID'] = positionNumber
	client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
	#print (sensor_data)
		
	client.loop_stop()
	client.disconnect()
	
def fetchData (positionNumber):
	global Name
	conn = sqlite3.connect('id.db')
	curs = conn.cursor()
	data = (positionNumber, )
	curs.execute("UPDATE employee SET time = datetime('now','localtime') WHERE id = (?)", data)
	curs.execute("SELECT Name FROM employee WHERE id = (?)", data)
	records = curs.fetchone()
	Name = records[0]
	#for row in records:
	    #print row
	    #Name = row
	    #print (Name)
	
	conn.commit()
	conn.close()
	
	
## Search for a finger
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to search the finger and calculate hash
while True:
    try:
        print('Waiting for finger...')
	#browserExe = "chromium-browse"
	#os.system("pkill "+browserExe )
	#webbrowser.open('/home/pi/Desktop/Fingerprint/Interface.html', new=0)

    ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

    ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
	    #browserExe = "chromium-browse"
	    #os.system("pkill "+browserExe)	    
	    #webbrowser.open('/home/pi/Desktop/Fingerprint/denied.html', new=0)
            time.sleep(2)
        else:
	    fetchData(positionNumber)
	    print("Welcome {}! Door is unlocked" .format(Name))
	    #browserExe = "chromium-browse"
	    #os.system("pkill "+browserExe)
	    #webbrowser.open('/home/pi/Desktop/Fingerprint/accept.html', new=0)
	    GPIO.output(17, False)
	    time.sleep(5)
	    GPIO.output(17, True)
	    #fetchData(positionNumber)
	    #print("Welcome {}! Door is unlocked" .format(Name))
            sendData()
	    

    except Exception as e:
	#raise
        print("Error! {}" .format(e))
        #print('Error message: ' + str(e))
        time.sleep(2)
        #exit(1)

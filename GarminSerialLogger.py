# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 13:10:42 2015

@author: 3820104
"""
import sys
import os
from threading import Thread
import serial
import time
import RPi.GPIO as GPIO
from time import sleep

#initialize serial connection
def init_serial():
    if(sys.platform.startswith('win')): # WINDOWS
        COMNUM = 6  # Set you COM port # here (Check it in device manager)
        global ser  # Must be declared in each fxn used
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = COMNUM -1 # Starts at 0, so subtract 1
        ser.timeout = 1 # You must specify a timeout (in seconds) so that the serial port doesn't hang
        ser.open() # Open the serial port
        # print port open or closed
    else :
        print "Opening RPi serial port."
        #sudo chmod 777 /dev/ttyAMA0
        ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1.0, rtscts=0)
    if ser.isOpen():
        print 'Open: ' + ser.portstr

def runWatcher(threadName, sleepTime):
    global kill_flag
    while 1 < 2:
        #time.sleep(sleepTime)

        # Needs to be BCM. GPIO.BOARD lets you address GPIO ports by periperal
        # connector pin number, and the LED GPIO isn't on the connector
        GPIO.setmode(GPIO.BCM)

        # set up GPIO output channel
        GPIO.setup(16, GPIO.OUT)

        # On
        GPIO.output(16, GPIO.LOW)

        # Wait a bit
        sleep(1)

        # Off
        GPIO.output(16, GPIO.HIGH)
        if(kill_flag > 0) :
            print threadName, " exiting."
            os.system('shutdown -h now')
            return

def runSerial():
    global kill_flag
    init_serial()
    f = open( '/media/GARMINGPS/gpsdata/' + time.strftime("%Y%m%d") + time.strftime("_%H_%M_%S") + '_nmea_strings.txt','w')
    #f = open( './gpsdata/' + time.strftime("%Y%m%d") + time.strftime("_%H_%M_%S") + '_nmea_strings.txt','w')
    while 1 < 2:
        # read what is on serial port
        data = ser.readline()   # reads in bytes followed by a newline
        if(len(data) > 1):
            f.write(data)
            if data.find('GPRMC') > -1 :
                print data
        else :
            print 'runSerial(): no data received, exiting.'
            f.close()
            ser.close()
            kill_flag = 1
            return


kill_flag = 0
threads=[]
if(os.path.exists('/dev/ttyUSB0')) :
    print 'starting serial ...'
    thread = Thread(target=runSerial, args=())
    threads.append(thread)
    thread.start()
    print 'starting watcher ...'
    thread = Thread(target=runWatcher, args=('runWatcher',2))
    threads.append(thread)
    thread.start()


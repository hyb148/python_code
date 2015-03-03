# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 13:10:42 2015

@author: 3820104
"""
import math
import os
from pynmea import nmea
import serial
import sys
from threading import Thread
from time import sleep
import time

if(sys.platform.startswith('win')==False):
    import RPi.GPIO as GPIO

#initialize serial connection
def init_serial(usehwd_flag=False):
    if(sys.platform.startswith('win')): # WINDOWS
        if(usehwd_flag):
            COMNUM = 6  # Set you COM port # here (Check it in device manager)
            global ser  # Must be declared in each fxn used
            ser = serial.Serial()
            ser.baudrate = 115200
            ser.port = COMNUM -1 # Starts at 0, so subtract 1
            ser.timeout = 1 # You must specify a timeout (in seconds) so that the serial port doesn't hang
            ser.open() # Open the serial port
            # print port open or closed
        else :
            ser = open(datadir + 'testdata.txt','r')
    else :
        print "Opening RPi serial port."
        #sudo chmod 777 /dev/ttyAMA0
        ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1.0, rtscts=0)
        if ser.isOpen():
            print 'Open: ' + ser.portstr
        else :
            exitnow('init_serial()')
        
def exitnow(name='no_name'):
    print name, " exiting."
    os.system('shutdown -h now')
    return
    
def runWatcher():
    # Needs to be BCM. GPIO.BOARD lets you address GPIO ports by periperal
    # connector pin number, and the LED GPIO isn't on the connector
    GPIO.setmode(GPIO.BCM)

    # set up GPIO output channel
    GPIO.setup(16, GPIO.OUT)

    while 1 < 2:
        # On
        GPIO.output(16, GPIO.LOW)
        # Wait a bit
        sleep(1)
        # Off
        GPIO.output(16, GPIO.HIGH)        
        #time.sleep(sleepTime)
        # Wait a bit
        sleep(1)
        

def lla2xyz(lat, lon, alt=0) :
    Re = 6378137
    Rp = 6356752.31424518
    
    latrad = lat/180.0*math.pi
    lonrad = lon/180.0*math.pi
    
    coslat = math.cos(latrad)
    sinlat = math.sin(latrad)
    coslon = math.cos(lonrad)
    sinlon = math.sin(lonrad)
    
    term1 = (Re*Re*coslat)/math.sqrt(Re*Re*coslat*coslat + Rp*Rp*sinlat*sinlat)
    
    term2 = alt*coslat + term1
    
    x=coslon*term2
    y=sinlon*term2
    z = alt*sinlat + (Rp*Rp*sinlat)/math.sqrt(Re*Re*coslat*coslat + Rp*Rp*sinlat*sinlat)
    return x,y,z

def fixDegrees(degs, dir='E') :
    """
    DDMM.MM => DD.DDDD
    #      4807.038,N   Latitude 48 deg 07.038' N
    #      01131.000,E  Longitude 11 deg 31.000' E
    """    
    dpoint = degs.find('.')
    """
    degs_f = float(degs[0:dpoint-2])
    mins_f = float(degs[dpoint-2:len(degs)])/60.
    print dpoint, degs[0:dpoint-2], degs_f, mins_f
    """
    if(dir=='S' or dir=='W'): sign = -1 
    else : sign = +1
    return sign*(float(degs[0:dpoint-2])+float(degs[dpoint-2:len(degs)])/60.)

def checkDelta(lat0,lon0,lat1,lon1):
    lat0 = fixDegrees(lat0)
    lon0 = fixDegrees(lon0)
    lat1 = fixDegrees(lat1)
    lon1 = fixDegrees(lon1)
    x0,y0,z0 = lla2xyz(lat0,lon0)
    x1,y1,z1 = lla2xyz(lat1,lon1)
    return math.sqrt((x0-x1)**2 + (y0-y1)**2)
    
def runSerial():
    global ser
    init_serial()
    nextstopfilename = 'nextstop.txt'
    gprmc = nmea.GPRMC()

    datafile = open( datadir + time.strftime("%Y%m%d") + time.strftime("_%H_%M_%S") + '_nmea_strings.txt','w')

    try:
        nextstopfile = open(datadir + nextstopfilename,'r')
        nextstop = nextstopfile.readline()
        nextstopfile.close()
        gprmc.parse(nextstop)
        nextstop_lat = gprmc.lat
        nextstop_lon = gprmc.lon
        nextstopsaved_flag = 0
    except:
        nextstop_lat = 0
        nextstop_lon = 0

    run_flag = 0
    while 1 < 2:
        # read what is on serial port
        data = ser.readline()   # reads in bytes followed by a newline
        if(len(data) > 1 and run_flag == 1):
            datafile.write(data)
            if data.find('GPRMC') > -1 :
                # if current loc < dist to end
                # write current for reverse trip
                if(nextstopsaved_flag==0):
                    nextstopfile = open(datadir + nextstopfilename,'w')
                    nextstopfile.write(data)
                    nextstopfile.close()
                    nextstopsaved_flag = 1

                if(nextstop_lat != 0):
                    gprmc.parse(data)
                    #if lat/lon delta < 100m exit then exit_flag = 1
                    delta = checkDelta(gprmc.lat,gprmc.lon,nextstop_lat,nextstop_lon)
                    print 'range = ', delta
                    if(delta < 50) :
                        run_flag = 0
        else :
            print 'runSerial(): no data received, exiting.'
            datafile.close()
            ser.close()
            exitnow('runSerial()')
            return


ser = [] # global serial object

if(sys.platform.startswith('win')==False): # Linux
    count = 0
    while(os.path.exists('/dev/ttyUSB0')==False) :
        if(count>10):
            exitnow('main()')
        else :
            print 'waiting for USB serial ...'
            count += 1
            sleep(1)
        exit
        
    datadir = '/media/GARMINGPS/gpsdata/'
    
    threads=[]
    print 'starting serial ...'
    thread = Thread(target=runSerial, args=())
    threads.append(thread)
    thread.start()
    print 'starting watcher ...'
    thread = Thread(target=runWatcher, args=())
    threads.append(thread)
    thread.start()
else :
    datadir = '../gpsdata/'
    runSerial()

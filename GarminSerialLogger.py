# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 13:10:42 2015

@author: 3820104
"""
import serial
import time
#initialize serial connection
def init_serial():
      COMNUM = 6  # Set you COM port # here (Check it in device manager)
      global ser  # Must be declared in each fxn used
      ser = serial.Serial()
      ser.baudrate = 115200
      ser.port = COMNUM -1 # Starts at 0, so subtract 1
      ser.timeout = 1 # You must specify a timeout (in seconds) so that the serial port doesn't hang
      ser.open() # Open the serial port
      # print port open or closed
      if ser.isOpen():
          print 'Open: ' + ser.portstr

init_serial()
f = open( time.strftime("%Y%m%d") + time.strftime("_%H_%M_%S") + '_nmea_strings.txt','w')
count = 10
while count > 0:
    # read what is on serial port
    data = ser.readline()   # reads in bytes followed by a newline
    f.write(data)
    if data.find('GPRMC') > -1 :
        print data
        count = count - 1
f.close()
ser.close()

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#NMEA sentences: http://www.gpsinformation.org/dale/nmea.htm
#example(this): https://helentronica.wordpress.com/2014/05/20/gps-module-python-google-maps-all-in-one/

from pynmea import nmea
import os

def fixDegrees(degs, dir='E') :
    """
    DDMM.MM => DD.DDDD
    #      4807.038,N   Latitude 48 deg 07.038' N
    #      01131.000,E  Longitude 11 deg 31.000' E
    """    
    dpoint = degs.find('.')
    #degs_f = float(degs[0:dpoint-2])
    #mins_f = float(degs[dpoint-2:len(degs)])/60.
    #print dpoint, degs[0:dpoint-2], degs_f, mins_f
    if(dir=='S' or dir=='W'): sign = -1 
    else : sign = +1
    return sign*(float(degs[0:dpoint-2])+float(degs[dpoint-2:len(degs)])/60.)

def txt2csv(txtfilename) :
    if(txtfilename.endswith('.txt')==False):
        print 'skipping: ', txtfilename
        return
    #print 'source', txtfilename[0:txtfilename.rfind('.')]
    csvfilename = txtfilename[0:txtfilename.rfind('.')+1] + 'csv'
    print 'writing to: ', csvfilename
    with open(csvfilename, "w") as outfile:
        with open(txtfilename, "r") as infile:
            outfile.write("time,lat,lon,spd,hdg\n")
            for line in infile:
            #print line.strip()
            
            # RMC - NMEA has its own version of essential gps pvt (position, velocity, time) data. It is called RMC, The Recommended Minimum, which will look similar to:
            # 
            # $GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
            # 
            # Where:
            #      RMC          Recommended Minimum sentence C
            #      123519       Fix taken at 12:35:19 UTC
            #      A            Status A=active or V=Void.
            #      4807.038,N   Latitude 48 deg 07.038' N
            #      01131.000,E  Longitude 11 deg 31.000' E
            #      022.4        Speed over the ground in knots
            #      084.4        Track angle in degrees True
            #      230394       Date - 23rd of March 1994
            #      003.1,W      Magnetic Variation
            #      *6A          The checksum data, always begins with *
            # Note that, as of the 2.3 release of NMEA, there is a new field in the RMC sentence at the end just prior to the checksum. For more information on this field see here.
                if line[0:6] == '$GPRMC' :
                    gprmc = nmea.GPRMC()
                    gprmc.parse(line)        
                    #print 'GPRMC - lat: ', gprmc.lat, 'lon: ', gprmc.lon, 'spd: ', gprmc.spd_over_grnd, 'hdg: ', gprmc.true_course
                    #print fixDegrees(gprmc.lat, gprmc.lat_dir), fixDegrees(gprmc.lon, gprmc.lon_dir)
                    data = gprmc.timestamp+','+str(fixDegrees(gprmc.lat, gprmc.lat_dir))+ ','+ str(fixDegrees(gprmc.lon, gprmc.lon_dir))+ ','+ gprmc.spd_over_grnd+ ','+ gprmc.true_course+'\n'
                    outfile.write(data)
                    #print data
        infile.close()
        outfile.close()

def list_files(path):
    # returns a list of names (with extension, without full path) of all files 
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files 
    
basepath = "../../gpsdata"
dirlisting = list_files(basepath)
for f in dirlisting:
    currentfile = basepath+'/'+f
    print currentfile    
    txt2csv(currentfile)

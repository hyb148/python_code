# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#NMEA sentences: http://www.gpsinformation.org/dale/nmea.htm
#example(this): https://helentronica.wordpress.com/2014/05/20/gps-module-python-google-maps-all-in-one/

from pynmea import nmea

array = []
with open("nema_strings.txt", "r") as f:
  for line in f:
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
        print 'GPRMC - lat: ', gprmc.lat, 'lon: ', gprmc.lon, 'spd: ', gprmc.spd_over_grnd, 'hdg: ', gprmc.true_course
 # GGA - essential fix data which provide 3D location and accuracy data.
# 
#  $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
# 
# Where:
#      GGA          Global Positioning System Fix Data
#      123519       Fix taken at 12:35:19 UTC
#      4807.038,N   Latitude 48 deg 07.038' N
#      01131.000,E  Longitude 11 deg 31.000' E
#      1            Fix quality: 0 = invalid
#                                1 = GPS fix (SPS)
#                                2 = DGPS fix
#                                3 = PPS fix
# 			       4 = Real Time Kinematic
# 			       5 = Float RTK
#                                6 = estimated (dead reckoning) (2.3 feature)
# 			       7 = Manual input mode
# 			       8 = Simulation mode
#      08           Number of satellites being tracked
#      0.9          Horizontal dilution of position
#      545.4,M      Altitude, Meters, above mean sea level
#      46.9,M       Height of geoid (mean sea level) above WGS84
#                       ellipsoid
#      (empty field) time in seconds since last DGPS update
#      (empty field) DGPS station ID number
#      *47          the checksum data, always begins with *
    if line[0:6] == '$GPGGA':
        gpgga = nmea.GPGGA()
        gpgga.parse(line)
        print 'GPGGA - lat: ', gpgga.latitude, ',lon: ', gpgga.longitude,\
        ',quality: ', gpgga.gps_qual, ',sats: ', gpgga.num_sats
        

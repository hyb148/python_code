# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 13:16:07 2015

@author: 3820104
"""

# convert lat/lon/alt (lat in degrees North, lon in degrees East, alt in meters) to earth centered fixed coordinates (x,y,z)
import math

def lla2xyz(lat, lon, alt=0) :
    Re = 6378137
    Rp = 6356752.31424518
    
    latrad = (lat/180.0)*math.pi
    lonrad = (lon/180.0)*math.pi
    
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

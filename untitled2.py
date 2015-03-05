# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 11:08:04 2015

@author: 3820104
"""

def mercToxy(lat,lon):
  r_major=6378137.000
  xm = r_major*math.radians(lon)
 
  if lat>89.5:lat=89.5
  if lat<-89.5:lat=-89.5
  r_major=6378137.000
  r_minor=6356752.3142
  temp=r_minor/r_major
  eccent=math.sqrt(1-temp**2)
  phi=math.radians(lat)
  sinphi=math.sin(phi)
  con=eccent*sinphi
  com=eccent/2
  con=((1.0-con)/(1.0+con))**com
  ts=math.tan((math.pi/2-phi)/2)/con
  ym=0-r_major*math.log(ts)
  return ym, xm
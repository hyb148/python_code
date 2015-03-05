# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 09:46:29 2015

@author: 3820104
"""

from matplotlib import pyplot as plt
import requests
from PIL import Image
from StringIO import StringIO
import math
from GlobalMercator import GlobalMercator

# https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/key-concepts.html#base-urls
def getTileXY(lat, lon, z) :
    latRad = lat * math.pi / 180
    n = math.pow(2, z)
    xTile = n * ((lon + 180) / 360)
    yTile = n * (1-(math.log(math.tan(latRad) + 1/math.cos(latRad)) / math.pi)) / 2
    # print latRad, n, xTile, yTile
    return int(math.floor(xTile)), int(yTile)

def getMapTile(xTile, yTile, z) :
    senddata = 'http://2.base.maps.cit.api.here.com/maptile/2.1/maptile/newest/normal.day/' + str(z) + '/' + str(xTile) + '/' + str(yTile) + '/256/png8?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg'
    print senddata
    r = requests.get(senddata)
    """
    print r.status_code
    print r.headers['content-type']
    print r.encoding
    4227.5132,N,08325.7081
    """
    return r

def GetAndShowTile(xT,yT,zoom):
    r = getMapTile(xT,yT,zoom)
    data = Image.open(StringIO(r.content))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(data)
    #plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    #plt.plot(lon,lat, 'o')
    plt.show()

##########################################################
# http://wiki.openstreetmap.org/wiki/Mercator
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
  return xm, ym    
##########################################################################
# original lat/lon to tile
def basicTileGet(lat, lon, zoom): 
    
    # Get Tile ID
    # http://docs.python-requests.org/en/latest/user/quickstart/
    xT, yT = getTileXY(lat,lon,zoom)
    print xT, yT
    """
    """
    
    # Get Tile from web and open as image
    GetAndShowTile(xT,yT,zoom)
    
###########################################################################     
# 2nd try at getting tile and having corner info
def TileGet2(lat, lon, zoom):
    gm = GlobalMercator()
    # check next function since MTT fails
    mx,my = gm.LatLonToMeters(lat,lon) # mercToxy() seems to verify it's okay.
    # compare results
    
    tx,ty = gm.MetersToTile(mx,my,5) # 2197,5165 - wrong
    GetAndShowTile(tx,ty,5)
    xT, yT = getTileXY(lat,lon,zoom) # 2197, 3026 - right
    GetAndShowTile(xT,yT,zoom)
    minx, miny, maxx, maxy = gm.TileBounds(tx,ty,zoom) # in meters
    px,py = gm.MetersToPixels(mx,my,zoom)
    
    print mx,my,px,py

#############################################################################    
# Start: we have the current position ...
lat = 42.475132 # Latitude
lon = -83.412081     # Longitude
zoom = 13              # Zoom level
 
# basicTileGet(lat, lon, zoom)   
TileGet2(lat,lon,zoom)
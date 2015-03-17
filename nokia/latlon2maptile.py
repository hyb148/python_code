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
from globalmaptiles import GlobalMercator

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
# used to check GlobalMercator function LatLonToMeters()
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
    # mx = -9285390.38293
    # my = 5232419.77888
    # compare results
    """
    tx,ty = gm.MetersToTile(mx,my,zoom) # 2197,5165 - wrong
    minx, miny, maxx, maxy = gm.TileBounds(tx,ty,zoom) # in meters
    GetAndShowTile(tx,ty,zoom)
    """
    xT, yT = getTileXY(lat,lon,zoom) # 2197, 3026 - right
    minx, miny, maxx, maxy = gm.TileBounds(xT, yT,zoom) # in meters
    GetAndShowTile(xT,yT,zoom)
    px,py = gm.MetersToPixels(mx,my,zoom)
    
    print mx,my,px,py

# http://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map
def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b
    
    #############################################################################
# 3rd try
def GetTileInfo(lat, lon, tz):
    # 13 42.475132 -83.412081
    # #python globalmaptiles.py 13 42.475132 -83.412081
    # Spherical Mercator (ESPG:900913) coordinates for lat/lon: (-9285390.382927291, 5232419.778884531)
    # 13/2197/5165 ( TileMapService: z / x / y )
    #         Google: 2197 3026
    #         Quadkey: 0302232030121 ( 13296409 )
    #         EPSG:900913 Extent:  (-9289850.66966718, 5229515.727158617, -9284958.69985693, 5234407.696968868)
    #         WGS84 Extent: (42.45588764197166, -83.45214843749999, 42.48830197960227, -83.408203125)
    #         gdalwarp -ts 256 256 -te -9289850.66967 5229515.72716 -9284958.69986 5234407.69697 
    #         <your-raster-file-in-epsg900913.ext> 13_2197_5165.tif
    mercator = GlobalMercator()
    mx, my = mercator.LatLonToMeters( lat, lon ) #Spherical Mercator (ESPG:900913) coordinates for lat/lon: (-9285390.382927291, 5232419.778884531)
    tx, ty = mercator.MetersToTile( mx, my, tz ) #13/2197/5165 ( TileMapService: z / x / y )
    #quadkey = mercator.QuadTree(tx, ty, tz) #Quadkey: 0302232030121 ( 13296409 )   
    #wgsbounds = mercator.TileLatLonBounds( tx, ty, tz) #WGS84 Extent: (42.45588764197166, -83.45214843749999, 42.48830197960227, -83.408203125)

    bounds = mercator.TileBounds( tx, ty, tz) #EPSG:900913 Extent:  (-9289850.66966718, 5229515.727158617, -9284958.69985693, 5234407.696968868)   
    llx,lly = mercator.MetersToPixels(bounds[0],bounds[1],tz) # 562432.0 1322240.0
    urx,ury = mercator.MetersToPixels(bounds[2],bounds[3],tz) # 562688.0 1322496.0
    
    px,py = mercator.MetersToPixels(mx,my,tz) # 562665.409741 1322391.97094
    px = 256 * (px-llx)/(urx-llx) #  plot x from 0
    py = 256 * (1 - (py-lly)/(ury-lly)) # plot y from -256
    #print px,py
    
    gx, gy = mercator.GoogleTile(tx, ty, tz) #Google: 2197 3026   
    r = getMapTile(gx,gy,tz)
    
    data = Image.open(StringIO(r.content))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(data)
    #plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.plot(px,py, marker='o', markerfacecolor='blue', markersize=.5) #'o')
    plt.show()
    
# Start: we have the current position ...
# http://teczno.com/squares/#13/42.475132/-83.412081
"""
Lat, lon: 42.4751, -83.4121
Mercator: -9285390, 5232420
Zoom: 13
Tile: 13/2197/3026
WKT’s: POINT (-83.4121 42.4751)
       POINT (-9285390 5232420)
"""
lat = 42.475132 # Latitude
lon = -83.412081     # Longitude
zoom = 13              # Zoom level
 
# basicTileGet(lat, lon, zoom)   
#TileGet2(lat,lon,zoom)
GetTileInfo(lat, lon, zoom)
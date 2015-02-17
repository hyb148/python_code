# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 12:07:05 2015

@author: 3820104
"""

import math

# http://gis.stackexchange.com/questions/46729/corner-coordinates-of-google-static-map-tile
tileSize = 256
initialResolution = 2 * math.pi * 6378137 / tileSize
# 156543.03392804062 for tileSize 256 pixels
originShift = 2 * math.pi * 6378137 / 2.0
# 20037508.342789244

def LatLonToMeters( lat, lon ):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"

        mx = lon * originShift / 180.0
        my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)

        my = my * originShift / 180.0
        return mx, my


def MetersToPixels( mx, my, zoom):
        "Converts EPSG:900913 to pyramid pixel coordinates in given zoom level"

        res = initialResolution / (2**zoom) #Resolution( zoom )
        px = (mx + originShift) / res
        py = (my + originShift) / res
        return px, py

def PixelsToMeters( px, py, zoom):
    "Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"

        # initialResolution / (2**zoom)
    res = initialResolution / (2**zoom) #Resolution(zoom)
    mx = px * res - originShift
    my = py * res - originShift
    return mx, my

def MetersToLatLon( mx, my ):
    "Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum"

    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0

    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
    return lon, lat


# 1)
# Dont forget you have to convert your projection to EPSG:900913
lat = 40.714728 #42.475132 # Latitude
lon = -73.998672 #-83.412081     # Longitude
mx,my = LatLonToMeters(lat,lon)
print 'mx', mx, ' my', my
zoom = 13              # Zoom level
#mx = -8237494.4864285 #-73.998672
#my = 4970354.7325767 # 40.714728

pixel_x, pixel_y = MetersToPixels( mx, my, zoom)

mx,my = PixelsToMeters( pixel_x, pixel_y, zoom)
llx, lly = MetersToLatLon( mx, my )


#Result
print llx, lly
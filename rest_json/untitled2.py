# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 16:04:25 2015

@author: 3820104
"""

import util
import json
from pprint import pprint

#import urllib
# Set the request URL
url = 'http://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&waypoint0=geo!52.5,13.4&waypoint1=geo!52.5,13.45&mode=fastest;car;traffic:disabled'

# Send the GET request
resp = util.request(url, 'XXX', 'XXX')
# Interpret the JSON response
data = json.loads(resp.decode('utf8'))
#print data
#http://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file-in-python
pprint(data)
#data["response"]["route|language|metaInfo]
#data["response"]["route"][0]["leg|mode|summary|waypoint"]
#data["response"]["route"][0]["leg"][0]["length|end|maneuver|start|travelTime"]
#len(data["response"]["route"][0]["leg"][0]["maneuver"])

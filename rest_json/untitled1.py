# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:50:20 2015

@author: 3820104
"""
#http://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&waypoint0=geo!52.5,13.4&waypoint1=geo!52.5,13.45&mode=fastest;car;traffic:disabled
import requests
import json
import pprint

senddata = 'http://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&waypoint0=geo!52.5,13.4&waypoint1=geo!52.5,13.45&mode=fastest;car;traffic:disabled'
r = requests.get(senddata)
print r.status_code
print r.headers['content-type']
print r.encoding
#print r.text
#print r.json()
data =  json.loads(r.text)
#print data
pprint(data)
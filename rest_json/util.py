import time
import datetime
import urllib2

def request(url, applicationID, applicationKey):
	
	# Set the request authentication headers
	timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d %H:%M:%S')
	headers = {'DecibelAppID': applicationID,
			   'DecibelAppKey': applicationKey,
			   'DecibelTimestamp': timestamp}

	# Send the GET request
	req = urllib2.Request(url, None, headers)

	# Read the response
	return urllib2.urlopen(req).read()
	
def formatTime(seconds):
	
	return time.strftime('%H:%M:%S', time.gmtime(seconds))
	
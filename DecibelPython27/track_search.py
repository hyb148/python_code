import util
import json
import urllib
import settings

def beginTrackSearch(trackTitle, applicationID, applicationKey):

	# Set the request URL
	url = settings.apiAddress + 'Tracks/?trackTitle=' + urllib.quote_plus(trackTitle) + '&format=json'

	# Send the GET request
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the collection of track objects
	return data['ResultSet']

# Search for tracks by name	
trackName = raw_input('Please enter a track name:')
result = beginTrackSearch(trackName, settings.applicationID, settings.applicationKey)

# Output the search results
for track in result:
	print(track['Name'] + ' - ' + track['Artists'])

raw_input('Press Enter to continue...')

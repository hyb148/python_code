import util
import json
import urllib
import settings

def beginWorkSearch(workName, applicationID, applicationKey):

	# Set the request URL
	url = settings.apiAddress + 'Works/?name=' + urllib.quote_plus(workName) + '&format=json'

	# Send the GET request
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the collection of track objects
	return data['ResultSet']

# Search for tracks by name	
workName = raw_input('Please enter a work name:')
result = beginWorkSearch(workName, settings.applicationID, settings.applicationKey)

# Output the search results
for work in result:
	print(work['Name'] + ' - ' + work['Composers'])

raw_input('Press Enter to continue...')
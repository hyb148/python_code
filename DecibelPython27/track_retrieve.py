import util
import json
import settings

def beginTrackRetrieve(trackID, applicationID, applicationKey):

	# Set the request URL
	depth = 'Names;Participations;ExternalIdentifiers;Genres;Performances;'
	url = settings.apiAddress + 'Tracks/?depth=' + depth + '&id=' + trackID + '&format=json'

	# Send the GET request
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the track object
	return data['ResultSet'][0]
	
# Retrieve track with participations	
result = beginTrackRetrieve('0703d0ef-73bf-40a3-888e-bae8bc96ca7a', settings.applicationID, settings.applicationKey)

# Output the results
print('Track Information:')
print('Name - ' + result['Name'])
print('Artists - ' + result['Artists'])
print('Track Number - ' + result['TrackNumber'])
print('Disc Number - ' + result['DiscNumber'])
print('Duration - ' + util.formatTime(result['TotalSeconds']))

print('Participations:');
for participant in result['Participations']:
	print(participant['Name']);

raw_input('Press Enter to continue...')


import util
import json
import settings

def beginWorkRetrieve(workID, applicationID, applicationKey):

	# Set the request URL
	depth = 'Annotations;ChartsAwards;Genres;Movements;Names;Nationalities;Publications;Publishers;'
	url = settings.apiAddress + 'Works/?depth=' + depth + '&id=' + workID + '&format=json'

	# Issue the request to the Decibel Web Service
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the participant object
	return data['ResultSet'][0]

def beginWorkTrackAppearances(workID, applicationID, applicationKey):

	# Set the request URL
	depth = 'Annotations;ChartsAwards;Genres;Movements;Names;Nationalities;Publications;Publishers;'
	url = settings.apiAddress + 'Works/' + workID + '/Tracks' + '?depth=' + depth + '&format=json'

	# Issue the request to the Decibel Web Service
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the collection of track appearances
	return data['ResultSet']
	
# Retrieve work with track appearances	
workID = 'a3ef26b4-0e82-426a-b1f8-18b23dbd22b2'
result = beginWorkRetrieve(workID, settings.applicationID, settings.applicationKey)
print('Name - ' + result['Name'])
print('Composers - ' + result['Composers'])
print('Catalogue - ' + result['Catalogue'])

result = beginWorkTrackAppearances(workID, settings.applicationID, settings.applicationKey)
print('Track Appearances:');
for trackAppearance in result:
	print(trackAppearance['TrackName'] + ' - ' + trackAppearance['TrackArtistName'] + ' - ' + trackAppearance['AlbumName'])

raw_input('Press Enter to continue...')


import util
import json
import settings

def beginParticipantRetrieve(participantID, applicationID, applicationKey):

	# Set the request URL
	depth = 'Names;GroupMembers;Nationalities;GeographicAreas;Annotations;ChartsAwards;Relationships;'
	url = settings.apiAddress + 'Participants/?depth=' + depth + '&id=' + participantID + '&format=json'

	# Send the GET request
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the participant object
	return data['ResultSet'][0]

def beginParticipantAssociates(participantID, applicationID, applicationKey):

	# Set the request URL
	depth = 'Names;GroupMembers;Nationalities;GeographicAreas;Annotations;ChartsAwards;Relationships;'
	url = settings.apiAddress + 'Participants/' + participantID + '/Associates?depth=' + depth + '&format=json'

	# Send the GET request
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the collection of participant associate objects
	return data['ResultSet']

def beginParticipantTrackAppearances(participantID, applicationID, applicationKey):

	# Set the request URL
	depth = 'Names;GroupMembers;Nationalities;GeographicAreas;Annotations;ChartsAwards;Relationships;'
	url = settings.apiAddress + 'Participants/' + participantID + '/Tracks?depth=' + depth + '&format=json'

	# Send the GET request
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the collection of track appearance objects
	return data['ResultSet']
	
participantID =	'fa94c7a0-cd68-48f3-b888-78a99733b60e'
result = beginParticipantRetrieve(participantID, settings.applicationID, settings.applicationKey)
print('Participant Name - ' + result['Name'])

result = beginParticipantAssociates(participantID, settings.applicationID, settings.applicationKey)
print('Associates:');
for associate in result:
	print(associate['Participant']['Name'])

result = beginParticipantTrackAppearances(participantID, settings.applicationID, settings.applicationKey)
print('Track Appearances:');
for trackAppearance in result:
	print(trackAppearance['TrackName'] + ' - ' + trackAppearance['AlbumName'])

raw_input('Press Enter to continue...')


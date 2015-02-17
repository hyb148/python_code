import util
import json
import settings

def beginAlbumRetrieve(albumID, applicationID, applicationKey):

	# Set the request URL
	depth = 'ExternalIdentifiers;Tracks;ImageThumbnail;Media;Names;Genres;Publications;Performances;'
	url = settings.apiAddress + 'Albums/?depth=' + depth + '&id=' + albumID + '&format=json'

	# Send the GET request
	resp = util.request(url, applicationID, applicationKey)

	# Interpret the JSON response 
	data = json.loads(resp.decode('utf8'))

	# Return the album object
	return data['ResultSet'][0]

# Retrieve album with track information	
result = beginAlbumRetrieve('d9675b59-7b88-40aa-9909-4e638839c799', settings.applicationID, settings.applicationKey)

# Output the results
print('Name - ' + result['Name'])
print('Artists - ' + result['Artists'])
print('Disc Count - ' + str(result['DiscCount']))
print('Track Count - ' + str(result['TrackCount']))
print('Duration - ' + util.formatTime(result['TotalSeconds']))

try:
	print('Format - ' + result['Discs'][0]['MusicMedium']['Name'])
except KeyError:
	pass

try:
	externalIdentifiers = result['ExternalIdentifiers']
	for externalIdentifier in externalIdentifiers:
		if externalIdentifier['ExternalDatabase']['Name'] == 'UPC Barcode':
			print('Barcode - ' + externalIdentifier['Identifier'])
			break
except KeyError:
	pass
	
try:
	genreValues = ''
	genres = result['Genres']
	for genre in genres:
		genreValues += genre['Genre']['Name'] + ', '
	print('Genres - ' + genreValues.rstrip(', '))
except KeyError:
	pass
	
try:
	print('Track List:')
	tracks = result['Tracks']
	for track in tracks:
		print(str(track['SequenceNo']) + ') ' + 
		track['Name'] + ' (' + util.formatTime(track['TotalSeconds']) + ')')
except KeyError:
	pass

raw_input('Press Enter to continue...')


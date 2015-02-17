import util
import base64
import settings

def beginAlbumArtRetrieve(albumID, applicationID, applicationKey):

	# Set the request URL
	url = settings.apiAddress + 'Albums/' + albumID + '/Image'

	# Send the GET request
	resp = util.request(url, applicationID, applicationKey)

	return '<img src="data:image/jpeg;base64,{0}">'.format(base64.b64encode(resp).decode('unicode_escape'))

result = beginAlbumArtRetrieve('5f754b70-c069-466e-a9c5-ae83ed638794', settings.applicationID, settings.applicationKey)

with open('album_art_retrieve.html', 'w') as the_file:
	the_file.write(result)
	
print('Album art written to album_art_retrieve.html')

raw_input('Press Enter to continue...')

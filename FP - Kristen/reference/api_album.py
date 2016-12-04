from flask import *
import dbquery

api_album = Blueprint('api_album', __name__, template_folder='templates')

@api_album.route('/album/<albumid>', methods=['GET'])
def api_album_route(albumid): # sensitive and public
	'''
	Sensitive pages with no session
	A user is not logged in and the resource is sensitive: 'You do not have the necessary credentials
	for the resource', 401*
	Sensitive pages with unauthorized access
	A user is logged in but does not have permissions to fetch/modify the resource: 'You do not have
	the necessary permissions for the resource', 403*
	'''

	'''
	GET /api/v1/album/<albumid> and /album?albumid=<albumid>
	The album must exist: 'The requested resource could not be found', 404*
	Proper authorization handling as specified above for sensitive pages*
	'''
	albumid = int(albumid)
	# the album must exist
	albumIDList = dbquery.getAlbumIDList()
	if albumid not in albumIDList:
		return jsonify(errors=dbquery.NOT_FOUND_404), 404
	
	# album has albumid, title, created, lastupdated, username, access
	album = dbquery.getAlbumByAlbumID(albumid=albumid)[0]

	### user is not logged in ###
	# if the user is not logged in and the album is private, 
	if 'username' not in session:
		if album['access'] == 'private':
			print 'username is not in session and album access is private'
			return jsonify(errors=dbquery.NOSESSION_401), 401
	
	### user is logged in ###
	# if the album is private and is not owned by user
	if album['access']=='private' and album['username']!=session['username']:
		usernameList = dbquery.getUsernameListFromAlbumAccess(albumid)
		# if the logged in user does not have access to the album, return 403 error
		if session['username'] not in usernameList:
			return jsonify(errors=dbquery.UNAUTHORIZED_403), 403

	# need to insert all pics 
	pics = []
	picIDList = dbquery.getPicIDListFromAlbumID(albumid=albumid)
	for picID in picIDList:
		# contain has albumid, picid, caption, sequencenum
		contain = dbquery.getContainByPicID(picid=picID)[0]
		# photo has picid, format, date
		photo = dbquery.getPhotoByPicID(picid=picID)[0]
		pics.append({'albumid':contain['albumid'], 'caption': contain['caption'], 'date':photo['date'], 'format':photo['format'], 'picid':photo['picid'], 'sequencenum':contain['sequencenum']})
	
	'''
	{
	"access": "public",
	"albumid": 1,
	"created": "2016-01-01 00:00:00",
	"lastupdated": "2016-02-02 00:00:00",
	"pics": [
	{
	"albumid": 1,
	"caption": "",
	"date": "2016-01-01",
	"format": "jpg",
	"picid": "5c00dd3598ce621105cb7062a59e7931",
	"sequencenum": 0
	},
	],
	"title": "I love sports",
	"username": "sportslover"
	}
	'''
	return jsonify(access=album['access'], albumid=albumid, created=album['created'], lastupdated=album['lastupdated'], pics=pics, title=album['title'], username=album['username'])

from flask import *
import dbquery

api_pic = Blueprint('api_pic', __name__, template_folder='templates')


@api_pic.route('/pic/<picid>', methods=['GET', 'PUT'])
def api_pic_route(picid):
	'''
	Sensitive pages with no session
	A user is not logged in and the resource is sensitive: 'You do not have the necessary credentials
	for the resource', 401*
	Sensitive pages with unauthorized access
	A user is logged in but does not have permissions to fetch/modify the resource: 'You do not have
	the necessary permissions for the resource', 403*
	'''

	'''
	GET /api/v1/pic/<picid> and /pic?picid=<picid>
	The pic must exist: 'The requested resource could not be found', 404*
	Proper authorization handling as specified above for sensitive pages*
	'''
	if request.method == 'GET': # sensitive / public
		# the pic must exist
		picIDList = dbquery.getPicIDList()
		if picid not in picIDList:
			return jsonify(errors=dbquery.NOT_FOUND_404), 404


		# contain has albumid, picid, caption, sequencenum
		contain = dbquery.getContainByPicID(picid=picid)[0]

		# album has albumid, title, created, lastupdated, username, access
		album = dbquery.getAlbumByAlbumID(contain['albumid'])[0]

		
		### user is not logged in ###
		# if the user is not logged in and the album is private, 
		if 'username' not in session:
			if album['access'] == 'private':
				return jsonify(errors=dbquery.NOSESSION_401), 401
		
		### user is logged in ###
		# if the album is private and is not owned by user
		if album['access']=='private' and album['username']!=session['username']:
			usernameList = dbquery.getUsernameListFromAlbumAccess(contain['albumid'])
			# if the logged in user does not have access to the album, return 403 error
			if session['username'] not in usernameList:
				return jsonify(errors=dbquery.UNAUTHORIZED_403), 403

		#User is logged in and the album is owned by user


		# photo has picid, format, date
		photo = dbquery.getPhotoByPicID(picid)[0]

		# if picidPrev or picidNext don't exist, return empty string
		picidPrev, picidNext = dbquery.getPrevNextPicIDFromPicID(picid=picid)

		print "picPrev:", picidPrev
		print "picNext:", picidNext

		'''
		OUTPUT JSON sample
		{
			"albumid" : 1,
			"caption" : "Pelle Pelle",
			"format" : "jpg",
			"next" : "5676..."
			"picid" : "43123421.."
			"prev" : "933 ...."	
		}
		'''
		return jsonify(albumid=contain['albumid'], caption=contain['caption'], format=photo['format'] , next=picidNext, picid=picid, prev=picidPrev)
	

		'''
		PUT /api/v1/pic/<picid> and /pic?picid=<picid>
		All fields are required: 'You did not provide the necessary fields', 422*
		This only occurs if a JSON key is missing from the request. If the key is there, but
		the value is the empty string, you should continue.
		The pic must exist: 'The requested resource could not be found', 404*
		Proper authorization handling as specified above for sensitive pages*
		Only caption is modifiable: 'You can only update caption', 403
		'''
	elif request.method == 'PUT': # sensitive
		'''
		PUT JSON sample
		{
			"albumid" : 1,
			"caption" : "Pelle Pelle",
			"format" : "jpg",
			"next" : "5676..."
			"picid" : "43123421.."
			"prev" : "933 ...."	
		}
		'''	
		picJSON = request.get_json()
		print 'received picJSON:', picJSON

		# All fields are required
		if 'albumid' not in picJSON:
			print 'albumid field required'
			return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		if 'caption' not in picJSON:
			print 'caption field required'
			return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		if 'format'	not in picJSON:
			print 'format field required'
			return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		if 'next' not in picJSON:
			print 'next field required'
			return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		if 'picid' not in picJSON:
			print 'picid field required'
			return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		if 'prev' not in picJSON:
			print 'prev field required'
			return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422

		# the pic must exist
		picIDList = dbquery.getPicIDList()
		# picid from api route
		if picid not in picIDList:
			return jsonify(errors=dbquery.NOT_FOUND_404), 404

		# contain has albumid, picid, caption, sequencenum
		contain = dbquery.getContainByPicID(picid=picid)[0]

		# album has albumid, title, created, lastupdated, username, access
		album = dbquery.getAlbumByAlbumID(contain['albumid'])[0]

		# photo has picid, format, date
		photo = dbquery.getPhotoByPicID(picid)[0]		

		# if picidPrev or picidNext don't exist, return empty string
		picidPrev, picidNext = dbquery.getPrevNextPicIDFromPicID(picid=picid)

		### user is not logged in ###
		# if the user is not logged in and the album is private, 
		if 'username' not in session:
			if album['access'] == 'private':
				return jsonify(errors=dbquery.NOSESSION_401), 401

		
		### user is logged in ###
		# if the album is private and is not owned by user
		if album['access']=='private' and album['username']!=session['username']:
			return jsonify(errors=dbquery.UNAUTHORIZED_403), 403

		ONLY_CAPTION_MODIFIABLE_403 =[{'message':'You can only update caption'}]
		# Only caption is modifiable	
		# if more than one field is modified, do we output one error message? or more than one error messages?
		# currently only output one error message	
		if picJSON['albumid'] != contain['albumid']:
			print 'albumid is different 403'
			return jsonify(errors=ONLY_CAPTION_MODIFIABLE_403), 403
		if picJSON['format'] != photo['format']:
			print 'format is different 403'
			return jsonify(errors=ONLY_CAPTION_MODIFIABLE_403), 403
		if picJSON['next'] != picidNext:
			print 'next is different 403'
			return jsonify(errors=ONLY_CAPTION_MODIFIABLE_403), 403
		if picJSON['picid'] != picid:
			print 'picid is different 403'
			return jsonify(errors=ONLY_CAPTION_MODIFIABLE_403), 403
		if picJSON['prev'] != picidPrev:
			print 'prev is different 403'
			return jsonify(errors=ONLY_CAPTION_MODIFIABLE_403), 403

		# db update caption
		dbquery.editCaptionByPicID(picid=picJSON['picid'], caption=picJSON['caption'])
		
		# On successful update, return a JSON object of the updated resource (same fields as those sent in the request) and a status code of 200
		return jsonify(picJSON), 200

	else :
		pass


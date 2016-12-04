from extensions import db
import datetime
import hashlib
import uuid


##### HTTP RESPONSE MESSAGE ######
UNAUTHORIZED_403 = [{'message': 'You do not have the necessary permissions for the resource'}]
NOSESSION_401 = [{'message':'You do not have the necessary credentials for the resource'}]
NOT_FOUND_404 = [{'message':'The requested resource could not be found'}]
NOT_ENOUGH_FIELD_422 = [{'message':'You did not provide the necessary fields'}]



##### ENCRYPTION #######
def encryptPassword(password):
	algorithm = 'sha512'
	salt = uuid.uuid4().hex
	m = hashlib.new(algorithm)
	m.update(salt + password)
	password_hash= m.hexdigest()
	return "$".join([algorithm, salt, password_hash])

def encryptPasswordWithSalt(password, dbpassword):
	algorithm = 'sha512'
	salt = dbpassword.rsplit('$', 2)[1]
	m = hashlib.new(algorithm)
	m.update(salt + password)
	password_hash= m.hexdigest()
	return "$".join([algorithm, salt, password_hash])



####### DB HELPER FUNCTION #########
# execute query string and return fetched result
def _dbresults(query):
	cur = db.cursor()
	cur.execute(query)
	return cur.fetchall()

# only execute query string without returning. Used when saving or deleting from database
def _dbexecute(query):
	cur = db.cursor()
	cur.execute(query)



###### USER TABLE #######

def getUserByUsername(username):
	query = 'SELECT * \
			FROM User \
			WHERE username="%s"' % (username)
	return _dbresults(query)

def getUsernameList():
	query = 'SELECT username \
			FROM User'
	usernames = _dbresults(query)
	usernameList = []
	for usernamedict in usernames:
		usernameList.append(usernamedict['username'])
	return usernameList

def insertUser(username, password, firstname, lastname, email):
	query = 'INSERT INTO User(username, password, firstname, lastname, email) \
			VALUES("%s", "%s", "%s", "%s", "%s")' % (username, password, firstname, lastname, email)
	_dbexecute(query)

def updateUserFirstname(firstname, username):
	query = 'UPDATE User \
			SET firstname="%s" \
			WHERE username="%s"' %(firstname, username)
	_dbexecute(query)

def updateUserLastname(lastname, username):
	query = 'UPDATE User \
			SET lastname="%s" \
			WHERE username="%s"' %(lastname, username)
	_dbexecute(query)

def updateUserPassword(password, username):
	query = 'UPDATE User \
			SET password="%s" \
			WHERE username="%s"' %(password, username)
	_dbexecute(query)

def updateUserEmail(email, username):
	query = 'UPDATE User \
			SET email="%s" \
			WHERE username="%s"' %(email, username)
	_dbexecute(query)	


###### ALBUM TABLE ######

# returns ex. ['1', '2', '3']
def getAlbumIDList():
	query = 'SELECT albumid \
			FROM Album'
	albumIDTuple = _dbresults(query)
	albumIDList = []
	for albumDict in albumIDTuple:
		albumIDList.append(int(albumDict['albumid']))
	return albumIDList

def getAlbumIDs():
	query = 'SELECT albumid \
			FROM Album'
	return _dbresults(query)

def getAlbumByAlbumID(albumid):
	query = 'SELECT * \
			FROM Album \
			WHERE albumid= "%d"' % (albumid)
	return _dbresults(query)

def getAlbumsByUsername(username):
	query = 'SELECT * \
			FROM Album \
			WHERE username= "%s"' % (username)
	return _dbresults(query)

def getAllPublicAlbums():
	query = 'SELECT * \
			FROM Album \
			WHERE access="public"'
	return _dbresults(query)

def getPublicAlbumsByUsername(username):
	query = 'SELECT * \
			FROM Album \
			WHERE access = "public" and username ="%s"' %(username)
	return _dbresults(query)

def getPrivateAlbumsByUsername(username):
	query = 'SELECT * \
			FROM Album \
			WHERE access = "private" and username ="%s"' %(username)
	return _dbresults(query)	

# All new albums have private access by default
def insertAlbum(title, username):
	query = 'INSERT INTO Album (title, username, access) \
			VALUES ("%s", "%s", "private");' % (title, username)
	_dbexecute(query)

def deleteAlbum(albumid):
	query = 'DELETE FROM Album \
			WHERE albumid= "%d"' % (albumid)
	_dbexecute(query)

def updateAlbumAccessByAlbumID(access, albumid):
	query = 'UPDATE Album \
			SET access = "%s" \
			WHERE albumid ="%d"' %(access, albumid)
	_dbexecute(query)

def updateAlbumLastupdatedByAlbumID(albumid):
	query = 'UPDATE Album \
			SET lastupdated = "%s" \
			WHERE albumid="%d"' %(datetime.datetime.now(), albumid)
	_dbexecute(query)



###### ALBUM ACCESS TABLE ######

def getAlbumAccessByAlbumID(albumid):
	query = 'SELECT * \
			FROM AlbumAccess \
			WHERE albumid ="%d"' %(albumid)
	return _dbresults(query)

def getUsernameListFromAlbumAccess(albumid):
	usernameList = []
	albumAccesses = getAlbumAccessByAlbumID(albumid)
	if albumAccesses == None:
		return usernameList

	for albumAccess in albumAccesses:
		usernameList.append(albumAccess['username'])
	return usernameList

def getAlbumAccessByUsername(username):
	query = 'SELECT * \
			FROM AlbumAccess \
			WHERE username ="%s"' %(username)
	return _dbresults(query)

def getAlbumIDListFromAlbumAccess(username):
	albumIDList = []
	albumAccesses = getAlbumAccessByUsername(username)
	if albumAccesses == None:
		return albumIDList

	for albumAccess in albumAccesses:
		albumIDList.append(albumAccess['albumid'])
	return albumIDList	

def insertAlbumAccess(username, albumid):
	query = 'INSERT INTO AlbumAccess \
			VALUES ("%d","%s")' %(albumid, username)
	_dbexecute(query)

def deleteAlbumAccess(username, albumid):
	query = 'DELETE FROM AlbumAccess \
			WHERE username="%s" and albumid = "%d"'%(username, albumid)
	_dbexecute(query)

def deleteAlbumAccessByAlbumID(albumid):
	query = 'DELETE FROM AlbumAccess \
			WHERE albumid = "%d"'%(albumid)
	_dbexecute(query)


###### PHOTO TABLE ######

def getPicIDs():
	query = 'SELECT picid \
			FROM Photo'
	return _dbresults(query)

def getPicIDList():
	picIDList = []
	picids = getPicIDs()
	for picid in picids:
		picIDList.append(picid['picid'])
	return picIDList

def getMaxSeq():
	query = 'SELECT max(sequencenum) \
			FROM Contain'
	return _dbresults(query)
	
def getPhotoByPicID(picid):
	query = 'SELECT * \
			FROM Photo \
			WHERE picid = "%s"' % (picid) 
	return _dbresults(query)

def insertPhoto(picid, format):
	query = 'INSERT INTO Photo (picid, format) \
			VALUES ("%s", "%s");' % (picid, format)
	_dbexecute(query)


def deletePhoto(picid):
	query = 'DELETE FROM Photo \
			WHERE picid = "%s"' % (picid)
	_dbexecute(query)


###### CONTAIN TABLE ######

def getContainByAlbumID(albumid):
	query = 'SELECT * \
			FROM Contain \
			WHERE albumid = "%s" \
			ORDER BY sequencenum' % (albumid)
	return _dbresults(query)

def getPicIDListFromAlbumID(albumid):
	contains = getContainByAlbumID(albumid)
	picIDList = []
	for contain in contains:
		picIDList.append(contain['picid'])
	return picIDList

def getContainByPicID(picid):
	query = 'SELECT * \
				FROM Contain \
				WHERE picid = "%s"' % (picid)
	return _dbresults(query)

def getSeqnums(albumid):
	query = 'SELECT sequencenum \
			FROM Contain \
			WHERE albumid = "%d" \
			ORDER BY sequencenum' % (albumid)
	return _dbresults(query)

def getPicidFromAlbumId(albumid):
	query = 'SELECT picid \
			FROM Contain \
			WHERE albumid = "%d" \
			ORDER BY sequencenum' % (albumid)
	return _dbresults(query)

def getPicidFromSeqnum(sequencenum):
	query = 'SELECT picid \
			FROM Contain \
			WHERE sequencenum = "%d"' % (sequencenum)
	return _dbresults(query)

def insertContain(sequencenum, albumid, picid, caption):
	query = 'INSERT INTO Contain (sequencenum, albumid, picid, caption) \
			VALUES ("%d", "%d", "%s", "%s");' % (sequencenum, albumid, picid, caption)
	_dbexecute(query)

def deleteContain(albumid, picid):
	query = 'DELETE FROM Contain \
			WHERE picid = "%s" and albumid = "%d"' % (picid, albumid)
	_dbexecute(query)

def editCaptionByPicID(picid, caption):
	query = 'UPDATE Contain SET caption = "%s" WHERE picid = "%s"' % (caption, picid) 
	_dbexecute(query)


######### PREV NEXT PICID ###########
def getPrevNextPicIDFromPicID(picid):
	contain = getContainByPicID(picid)[0]
	picidList = getPicIDListFromAlbumID(contain['albumid'])

	index = picidList.index(picid)

	picidPrev = ''
	picidNext = ''
	if index != 0:
		picidPrev = picidList[index-1]
	if index < len(picidList) - 1:
		picidNext = picidList[index+1]

	return picidPrev, picidNext


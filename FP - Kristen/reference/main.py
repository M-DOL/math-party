from flask import *
import dbquery

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():

	publicAlbums = dbquery.getAllPublicAlbums()
	usernameList = dbquery.getUsernameList()

	privateAlbums = None
	grantedAlbums = None

	if 'username' in session:
		username = session['username']
		privateAlbums = dbquery.getPrivateAlbumsByUsername(username)
		albumIDList = dbquery.getAlbumIDListFromAlbumAccess(username)
		grantedAlbums = []
		for albumID in albumIDList:
			grantedAlbums.append(dbquery.getAlbumByAlbumID(albumID)[0])

	# make sure to pass session variable
	return render_template("index.html", usernameList=usernameList, publicAlbums=publicAlbums, privateAlbums=privateAlbums, grantedAlbums=grantedAlbums, session=session)
	
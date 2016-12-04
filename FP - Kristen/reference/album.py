from flask import *
import dbquery
import os

app = Flask(__name__)



@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
	options = {
		"edit": True
	}

	return render_template("album.html", albumid=albumid, album=album, usernameList = usernameList, photos=photos, session=session, **options)



@album.route('/album')
def album_route():
		
	return render_template("album.html")

from flask import *
import dbquery

app = Flask(__name__)

teacher = Blueprint('teacher', __name__, template_folder='templates')

@teacher.route('/teacher')
def teacher_route():
		
	return render_template("teacher.html")

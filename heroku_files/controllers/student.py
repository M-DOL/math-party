from flask import *
import dbquery

app = Flask(__name__)

student = Blueprint('student', __name__, template_folder='templates')

@student.route('/student')
def student_route():
	return render_template("student.html")

from flask import *
import dbquery

app = Flask(__name__)

teacher = Blueprint('teacher', __name__, template_folder='templates')

@teacher.route('/teacher',  methods=['GET', 'POST'])
def teacher_route():
	
	if request.method == 'POST':
		dbquery.emptyClass()



	return render_template("teacher.html")


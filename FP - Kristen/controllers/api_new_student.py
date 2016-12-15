import dbquery
from flask import *



api_new_student = Blueprint('api_new_student', __name__, template_folder='templates')

@api_new_student.route('/api_new_student', methods=['POST'])
def api_new_student_route():
	
		'''
		POST JSON sample
		{
			"name" : "Peter Parker"
		}
		'''	

		
		studentJSON = request.get_json()
		print 'received student:', studentJSON

		studentList = dbquery.getStudentList()

		# insert student into class if not entered yet
		if studentJSON['name'] not in studentList:
			dbquery.insertStudent(studentJSON['name'])

		studentJSONupdated = dbquery.getStudent(studentJSON['name'])[0]
		print 'updated student:', studentJSONupdated

		# On successful update, return a status code of 200
		return jsonify(studentJSONupdated), 200
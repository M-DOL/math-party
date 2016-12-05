import dbquery
from flask import *



api_new_student = Blueprint('api_new_student', __name__, template_folder='templates')

@api_new_student.route('/api_new_student', methods=['PUT'])
def api_new_student_route():
	
		'''
		PUT JSON sample
		{
			"name" : "Peter Parker"
		}
		'''	
		studentJSON = request.get_json()
		print 'received student:', studentJSON

		# All fields are required
		# if 'name' not in studentJSON:
		# 	print 'name field required'
		# 	return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		
		# studentList = dbquery.getStudentList()

		# # insert student into class if not entered yet
		# if studentJSON['name'] not in studentList:
		# 	insertStudent(studentJSON['name'])
		
		# On successful update, return a status code of 200
		return jsonify(studentJSON), 200
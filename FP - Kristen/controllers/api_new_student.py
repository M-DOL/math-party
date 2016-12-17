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
		print studentList

		# # insert student into class if not entered yet
		if studentJSON['name'] not in studentList:
			dbquery.insertStudent(studentJSON['name'])

		studentUpdated = dbquery.getStudent(studentJSON['name'])[0]
		
		studentJSONupdated = {}
		studentJSONupdated['name'] = studentUpdated[0]
		studentJSONupdated['num_correct'] = studentUpdated[1]
		studentJSONupdated['num_attempted'] = studentUpdated[2]
		studentJSONupdated['avg_time'] = studentUpdated[3]
		studentJSONupdated['right_in_a_row'] = studentUpdated[4]
		studentJSONupdated['badge_1'] = studentUpdated[5]
		studentJSONupdated['badge_2'] = studentUpdated[6]
		studentJSONupdated['badge_3'] = studentUpdated[7]

		print 'updated student:', studentJSONupdated

		# On successful update, return a status code of 200
		return jsonify(studentJSONupdated), 200
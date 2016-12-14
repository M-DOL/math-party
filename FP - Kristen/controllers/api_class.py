from flask import *
import dbquery


api_class = Blueprint('api_class', __name__, template_folder='templates')

@api_class.route('/api_class', methods=['GET', 'PUT'])
def api_class_route():
	
	if request.method == 'GET':
			
		'''	
		GET JSON sample
		{
			"students" :	[
					{
						"name" : "Peter Parker",
						"num_correct" : 10,
						"num_attempted" : 11,
						"avg_time" : 30,
						"right_in_a_row": 3,
						"badge_1" : false, # has not yet earned first badge
						"badge_2" : false,
						"badge_3" : false
					},

					{
						"name" : "Mary Jane Watson",
						"num_correct" : 12,
						"num_attempted" : 15,
						"avg_time" : 25,
						"right_in_a_row": 3,
						"badge_1" : true, # has earned first badge
						"badge_2" : false,
						"badge_3" : false
					}

				]
		}
		'''


		classList = {}
		classList['students'] = dbquery.getClass()

		return jsonify(classList), 200


	elif request.method == 'PUT': 
		
		'''
		PUT JSON sample
		{
			"name" : "Peter Parker",
			"result" : 1,	# 1 for correct, 0 for incorrect
			"time" : 35 	# time in seconds spent on the problem
		}
		'''	


		studentJSON = request.get_json()
		print 'received student:', studentJSON

		# TODO implement badges update
		dbquery.updateStudent(studentJSON['name'], studentJSON['result'], studentJSON['time'])

		studentJSONupdated = dbquery.getStudent(studentJSON['name'])[0]
		print 'updated student:', studentJSONupdated

		# On successful update, return a status code of 200
		return jsonify(studentJSONupdated), 200

	else :
		pass


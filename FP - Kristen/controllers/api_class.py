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
						# "badges" : {

						# 	# TODO

						# }
					},

					{
						"name" : "Mary Jane Watson",
						"num_correct" : 12,
						"num_attempted" : 15,
						"avg_time" : 25,
						# "badges" : {

						# 	# TODO

						# }
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
			"result" : 1,	# 0 for incorrect
			"time" : 35, 	# time in seconds spent on the problem
			"badges" : {

				# TODO

			}
		}
		'''	

		studentJSON = request.get_json()
		print 'received student:', studentJSON

		# TODO implement badges update
		dbquery.updateStudent(studentJSON['name'], studentJSON['result'], studentJSON['time'])
		
		# On successful update, return a status code of 200
		return jsonify(studentJSON), 200

	else :
		pass


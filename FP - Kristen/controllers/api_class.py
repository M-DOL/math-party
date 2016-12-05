from flask import *
import dbquery


api_class = Blueprint('api_class', __name__, template_folder='templates')

@api_class.route('/api_class', methods=['GET', 'PUT'])
def api_class_route():
	
	if request.method == 'GET':
		
		# classList = dbquery.getClass()

		# return jsonify(classList), 200


		classList = {

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

		# # All fields are required
		# if 'name' not in studentJSON:
		# 	print 'name field required'
		# 	return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		# if 'result' not in studentJSON:
		# 	print 'result field required'
		# 	return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		# if 'time' not in studentJSON:
		# 	print 'time field required'
		# 	return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		
		# TODO badges
		# if 'badges' not in studentJSON:
		# 	print 'badges field required'
		# 	return jsonify(errors=dbquery.NOT_ENOUGH_FIELD_422), 422
		
		# """ OPTIONAL ERROR HANDLING """
		# # get the roster
		# studentList = dbquery.getStudentList()

		# # make sure student in class
		# if studentJSON['name'] not in studentList:
		# 	return jsonify(errors=NOT_FOUND_404), 404

		# """ END OPTIONAL ERROR HANDLING """

		# TODO implement badges update
		dbquery.updateStudent(studentJSON['name'], studentJSON['result'], studentJSON['time'])
		
		# On successful update, return a status code of 200
		return jsonify(studentJSON), 200

	else :
		pass


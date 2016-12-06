from extensions import db


####### HTTP RESPONSE MESSAGE #######
NOT_ENOUGH_FIELD_422 = [{'message':'You did not provide the necessary fields'}]
NOT_FOUND_404 = [{'message':'The requested resource could not be found'}]


####### DB HELPER FUNCTION #########
# execute query string and return fetched result
def _dbresults(query):
	cur = db.cursor()
	cur.execute(query)
	return cur.fetchall()

# only execute query string without returning. Used when saving or deleting from database
def _dbexecute(query):
	cur = db.cursor()
	cur.execute(query)


###### USER TABLE #######

def getClass():
	query = 'SELECT * \
			FROM Class'
	return _dbresults(query)

def insertStudent(name):
	# initalize student entry
	query = 'INSERT INTO Class(name, num_correct, num_attempted, avg_time) \
			VALUES("%s", 0, 0, 0)' % (name)
	_dbexecute(query)

def updateStudent(name, result, time):
	print("updateStudent")
	# get the specified student
	query = 'SELECT * \
			FROM Class \
			WHERE name="%s"' %(name)
	studentTuple = _dbresults(query)
	
	# update the student information
	student = studentTuple[0]
	new_num_correct = student['num_correct'] + result
	new_num_attempted = student['num_attempted'] + 1
	new_avg_time = (student['avg_time'] + time) / new_num_attempted

	query = 'UPDATE Class SET num_correct=%s, num_attempted=%s, avg_time=%s WHERE name="%s"' % (new_num_correct, new_num_attempted, new_avg_time, name)
	_dbexecute(query)

def getStudentList():
	query = 'SELECT * \
			FROM Class'
	classTuple = _dbresults(query)
	studentList = []
	# loop through all student objects and build dictionary of names
	for studentDict in classTuple:
		studentList.append(studentDict['name'])
	return studentList	


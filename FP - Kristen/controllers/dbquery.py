#from extensions import db
import sqlite3

####### HTTP RESPONSE MESSAGE #######
NOT_ENOUGH_FIELD_422 = [{'message':'You did not provide the necessary fields'}]
NOT_FOUND_404 = [{'message':'The requested resource could not be found'}]
conn = sqlite3.connect('/Users/Fritz/Desktop/EECS 493/math-party/FP - Kristen/DB/final_project.db', check_same_thread=False)
conn.isolation_level = None

####### DB HELPER FUNCTION #########
# execute query string and return fetched result
def _dbresults(query):
	cur = conn.cursor()
	cur.execute(query)
	return cur.fetchall()

# only execute query string without returning. Used when saving or deleting from database
def _dbexecute(query):
	cur = conn.cursor()
	cur.execute(query)

###### Class TABLE #######

def getClass():
	query = 'SELECT * \
			FROM Class'
	return _dbresults(query)

def getStudent(name):
	query = 'SELECT * \
			FROM Class \
			WHERE name="%s"' % (name)
	return _dbresults(query)

def insertStudent(name):
	# initalize student entry
	query = 'INSERT INTO Class(name, num_correct, num_attempted, avg_time, right_in_a_row, badge_1, badge_2, badge_3) \
			VALUES("%s", 0, 0, 0, 0, 0, 0, 0)' % (name)
	_dbexecute(query)

def updateStudent(name, result, time):
	# get the specified student
	query = 'SELECT * \
			FROM Class \
			WHERE name="%s"' % (name)
	studentTuple = _dbresults(query)
	
	# name, num_correct, num_attempted, avg_time, right_in_a_row, badge_1, badge_2, badge_3

	# update the student information
	student = studentTuple[0]
	new_num_correct = student[1] + result
	new_num_attempted = student[2] + 1
	new_avg_time = ((student[3] * student[2]) + time) / new_num_attempted

	new_right_in_a_row = 0

	# if student gets a question right, update right_in_a_row 
	if result == 1:
		new_right_in_a_row = student[4] + 1

	# note badge status
	new_badge_1 = student[5]
	new_badge_2 = student[6]
	new_badge_3 = student[7]

	# if student has 7 right in a row, give the student the next badge
	if new_right_in_a_row == 7:
		if not student[5]:
			new_badge_1 = 1
			new_right_in_a_row = 0
		elif not student[6]:
			new_badge_2 = 1
			new_right_in_a_row = 0
		elif not student[7]:
			new_badge_3 = 1

	query = 'UPDATE Class \
			SET num_correct=%s, num_attempted=%s, avg_time=%s, right_in_a_row=%s, badge_1=%s, badge_2=%s, badge_3=%s \
			WHERE name="%s"' % (new_num_correct, new_num_attempted, new_avg_time, new_right_in_a_row, new_badge_1, new_badge_2, new_badge_3, name)
	_dbexecute(query)

def getStudentList():
	query = 'SELECT * \
			FROM Class'
	
	students = _dbresults(query)
	print(students)
	studentNames = []
	for i in students:
		studentNames.append(i[0])
	return studentNames



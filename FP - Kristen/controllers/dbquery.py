
'''
from extensions import db
'''

####### HTTP RESPONSE MESSAGE #######
NOT_ENOUGH_FIELD_422 = [{'message':'You did not provide the necessary fields'}]
NOT_FOUND_404 = [{'message':'The requested resource could not be found'}]


####### DB HELPER FUNCTION #########
# execute query string and return fetched result
def _dbresults(query):
	print("dbresults")
	# cur = db.cursor()
	# cur.execute(query)
	# return cur.fetchall()

# only execute query string without returning. Used when saving or deleting from database
def _dbexecute(query):
	print("dbexecute")
	# cur = db.cursor()
	# cur.execute(query)


###### USER TABLE #######

def getClass():
	print("getClass")
	# query = 'SELECT * \
	# 		FROM Class'
	# return _dbresults(query)

def insertStudent(name):
	print("insertStudent")
	# query 
	# _dbexecute(query)

def updateStudent(name, result, time):
	print("updateStudent")
	# query 
	# _dbexecute(query)

def getStudentList():
	print("getStudentList")
	#query
	# _dbexecute(query)


import sqlite3
import trackerDBoperations
from bottle import route , run, request, template


@route('/')
def homePage():
    return """
		<html>
		Welcome to your personal Tracker To Do list
		<br></br>
		<br><a href="http://localhost:9999/addPlanform">Add New Plan</a></br>
		<br><a href="http://localhost:9999/listPlan">List Plan</a></br>
		<br><a href="http://localhost:9999/modifyPlan">Update Plan</a></br>
		<br><a href="http://localhost:9999/deleteExpPlan">Delete expired Plan</a></br>
		</html>
		"""

@route('/addPlanform')
def addPlanform():
    return """
<html>
<form method=post action="http://localhost:9999/addPlan">
<input type=text name=targetTimeStamp>Target TimeStamp "YYYY-MM-DD HH:MM:SS"<br>
<input type=text name=plan>Enter your plan<br>
<input type=submit>
</form>
</html>
    """

@route('/addPlan',method='POST')
def addPlan():
	targetTimeStamp = request.forms.get('targetTimeStamp')
	plan = request.forms.get('plan')
	trackerDBoperations.TrackerDbOperations().addPlan(targetTimeStamp,plan)
	return """Plan added  !!
	<br><a href="http://localhost:9999/">Home Page</a></br>
	"""
	
@route('/listPlan')
def listPlan():
    output="""<style>
	table {border-collapse: collapse;width: 100%;}
	th, td {text-align: left;padding: 8px;}
	tr:nth-child(even){background-color: #f2f2f2}
	</style>
	<table border=1>
	<h1>To Do List</h1>
	<tr><th>ID</th><th>CreateDate</th><th>ModifiedDate</th><th>TargetDate</th><th>Plan</th>
	</tr>"""
    tablerow="""<tr>
	<td>{}</td>
	<td>{}</td>
	<td>{}</td>
	<td>{}</td>
	<td>{}</td>
	</tr>"""
    for id,createDate,modifiedDate,targetDate,plan in trackerDBoperations.TrackerDbOperations().listPlan():
        output += tablerow.format(id,createDate,modifiedDate,targetDate,plan)
    output+="</table>"
    return output + """
	<br><a href="http://localhost:9999/">Home Page</a></br>
	"""


@route('/modifyPlan')
def modifyPlan():
	output="""<style>
	table {border-collapse: collapse;width: 100%;}
	th, td {text-align: left;padding: 8px;}
	tr:nth-child(even){background-color: #f2f2f2}
	</style>
	<table id="list" border=1>
	<h1>To Do List</h1>
	<tr><th>ID</th><th>CreateDate</th><th>ModifiedDate</th><th>TargetDate</th><th>Plan</th>
	</tr>"""
	tablerow="""
	<tr>
	<td>{}</td>
	<td>{}</td>
	<td>{}</td>
	<td contenteditable='true'>{}</td>
	<td contenteditable='true'>{}</td>
	<td><a href="http://localhost:9999/deletePlan/{}">delete</a></td>
	<td><a href="http://localhost:9999/updatePlan/{},{},{}/">Update</a></td>
	</tr>"""
	# find a way to read the the data from the updated row. functionality still missing.
	for id,createDate,modifiedDate,targetDate,plan in trackerDBoperations.TrackerDbOperations().listPlan():
		output += tablerow.format(id,createDate,modifiedDate,targetDate,plan,id,targetDate.replace('/','-'),plan,id)
	output+="""</table>
	"""
	return output + """
	<br><a href="http://localhost:9999/">Home Page</a></br>
	"""

@route('/deletePlan/<id>')
def deletePlan(id):
	trackerDBoperations.TrackerDbOperations().deletePlan(id)
	goBack = """
	<caption><br>plan {} deleted</br></caption>
	<br><a href="http://localhost:9999/modifyPlan">go Back</a></br>
	<br><a href="http://localhost:9999/">Home Page</a></br>
	""".format(id)
	return goBack

@route('/updatePlan/<targetDate>,<plan>,<id>/')
def updatePlan(targetDate,plan,id):
	trackerDBoperations.TrackerDbOperations().updatePlan(targetDate,plan,id)
	goBack = """
	<caption><br>plan {} update</br></caption>
	<br><a href="http://localhost:9999/modifyPlan">go Back</a></br>
	<br><a href="http://localhost:9999/">Home Page</a></br>
	""".format(id)
	return goBack
	
@route('/deleteExpPlan')
def deleteExpPlan():
	trackerDBoperations.TrackerDbOperations().deleteExpiredplan()
	return "done !!"
	
run(host='localhost',port=9999,debug=True)

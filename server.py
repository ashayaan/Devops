from flask import Flask, flash, redirect, render_template, request, session, abort
from flaskext.mysql import MySQL
import os
import time

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Shayaan7'
app.config['MYSQL_DATABASE_DB'] = 'devops'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		return render_template("home.html")


@app.route('/editbook',methods=['GET', 'POST'])
def editBooks():
	isbn = request.form["ISBN"]
	title = request.form["title"]
	author = request.form["author"]
	description = request.form["description"]
	book_type = request.form["type"]
	conn = mysql.connect()
	cursor =conn.cursor()
	cursor.execute("UPDATE books set name='"+title+"', author='"+author+"', description='"+description+"', time_added='"+time.strftime('%Y-%m-%d')+"',type='"+book_type+"' where user_id='"+str(session['ID'])+"' and ISBN='"+isbn+"'")
	conn.commit()
	# print author,isbn
	return booksAdded()

@app.route('/request_add', methods=['GET','POST'])
def addRequest():
	req = request.form["request"]
	conn = mysql.connect()
	cursor = conn.cursor()
	print req
	query = "INSERT INTO requests(user_id,requests) " \
			"VALUES(%s,%s)"
	data = (session['ID'],req)
	cursor.execute(query,data)
	conn.commit()
	return home()

@app.route('/view_request', methods=['GET','POST'])
def viewRequest():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT users.Name, users.email,users.number,requests.requests from users,requests where users.ID = requests.user_id")
	data = cursor.fetchall()
	print data
	return home()



@app.route('/delbook',methods=['GET', 'POST'])
def deleteBooks():
	isbn = request.form["ISBN"]
	conn = mysql.connect()
	cursor =conn.cursor()
	cursor.execute("DELETE from books where user_id='"+str(session['ID'])+"' and ISBN='"+isbn+"'")
	conn.commit()
	# print author,isbn
	return booksAdded()

@app.route('/profile')
def profile():
	conn = mysql.connect()
	cursor =conn.cursor()
	cursor.execute("SELECT * from users where username='" + session['username'] + "'")
	data = cursor.fetchone() 
	session['name'] = data[1]
	session['password'] = data[3]
	session['email'] = data[4]
	session['number'] = data[5]
	return render_template("profile.html")

@app.route('/books_added')
def booksAdded():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT ISBN,name,author,description, type from books where user_id='"+str(session['ID'])+"'")
	data = cursor.fetchall()
	# print data
	return render_template("books_added.html",result = data)


@app.route('/editNumber', methods=['GET', 'POST'])
def editNumber():
	no = request.form['number']
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("UPDATE users set number ='"+no+"' where ID='"+str(session['ID'])+"'")
	conn.commit()
	return profile()

@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
	opass = request.form['opassword']
	npass = request.form['npassword']
	rnpass = request.form['rnpassword']

	if (opass != session['password']):
		error = 'Old Password did not match'
		return render_template('profile.html',error=error)
	elif (npass != rnpass):
		error = 'New password did not match each other'
		return render_template('profile.html',error=error)
	else:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("UPDATE users set password ='"+npass+"' where ID='"+str(session['ID'])+"'")
		conn.commit()
		return profile()

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/signin')
def signin():
	return render_template('signin.html')

@app.route('/signUp',methods=['POST'])
def signUp():
	query = "INSERT INTO users(ID,Name,username,password,email) " \
			"VALUES(%s,%s,%s,%s,%s)"
	name = request.form['name']
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	conn = mysql.connect()
	cursor = conn.cursor()
	if name and username and password and email:
		isdata = (0,name,username,password,email)
		cursor.execute("SELECT * from users where username='" + username + "'")
		data = cursor.fetchone()
		if data is None:
			print isdata
			cursor.execute(query,isdata)
			conn.commit()
			return render_template("signin.html")
		else:
			error = 'Username already existts'
			return render_template('signup.html',error=error)
	else:
		error = 'Enter all the details'
		return render_template('signup.html',error=error)



@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
	password = request.form['password']
	username = request.form['username']
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from users where username='" + username + "' and password='" + password + "'")
	data = cursor.fetchone()
	if data is None:
		session["logged_in"]=False
		error = 'Username or Password Wrong!'
		return render_template('signin.html',error=error)
	else:
		session['logged_in'] = True
		session['ID'] = data[0]
		session['username'] = username
		return home()

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return home()
	
if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug = True,host= '0.0.0.0')
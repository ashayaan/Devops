from flask import Flask, flash, redirect, render_template, request, session, abort
from flaskext.mysql import MySQL
from flask_mail import Mail
# from flask_security import Security
import os
import time
import logging	
from passlib.hash import sha256_crypt


mysql = MySQL()
mail = Mail()
# security = Security()
app = Flask(__name__)
# Database configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Shayaan7'
app.config['MYSQL_DATABASE_DB'] = 'devops'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'buzzshayaan@gmail.com'
app.config['MAIL_PASSWORD'] = 'shayaan7'
# Security configuration
app.config['SECURITY_RECOVERABLE'] = True


mysql.init_app(app)
mail.init_app(app)
# security.init_app(app)

app.secret_key = os.urandom(12)

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

@app.route('/addbook',methods=['GET','POST'])
def addBook():
	if request.method == 'GET':
		return render_template("addbook.html")
	elif request.method == 'POST':
		query = "INSERT into books(user_id,ISBN,name,author,description,time_added,type)"\
				"VALUES(%s,%s,%s,%s,%s,%s,%s)"
		conn = mysql.connect()
		cursor =conn.cursor()
		data = (str(session['ID']),request.form["ISBN"],request.form["name"],request.form["author"],request.form["description"],time.strftime('%Y-%m-%d'),request.form["type"])
		cursor.execute(query,data)
		conn.commit()
		return booksAdded()


@app.route('/delbook',methods=['GET', 'POST'])
def deleteBooks():
	isbn = request.form["ISBN"]
	conn = mysql.connect()
	cursor =conn.cursor()
	cursor.execute("DELETE from books where user_id='"+str(session['ID'])+"' and ISBN='"+isbn+"'")
	conn.commit()
	# print author,isbn
	return booksAdded()

@app.route('/books_added')
def booksAdded():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT ISBN,name,author,description, type from books where user_id='"+str(session['ID'])+"'")
	data = cursor.fetchall()
	# print data
	return render_template("books_added.html",result = data)

@app.route('/findbook', methods=['GET','POST'])
def findBook():
	conn = mysql.connect()
	cursor = conn.cursor()
		
	if request.method == 'GET':
		cursor.execute("SELECT books.name,books.author, users.Name,users.email,users.number,books.time_added from users, books where users.ID = books.user_id;")
		data = cursor.fetchall()
		return render_template("findbook.html",result = data)
	elif request.method == 'POST':
		search = request.form['search']
		criteria = request.form['criteria']
		if criteria == 'name':
			cursor.execute("SELECT books.name,books.author, users.Name,users.email,users.number,books.time_added from users, books where users.ID = books.user_id and books.name='"+search+"'")
			data = cursor.fetchall()
		else:
			cursor.execute("SELECT books.name,books.author, users.Name,users.email,users.number,books.time_added from users, books where users.ID = books.user_id and books.author='"+search+"'")
			data = cursor.fetchall()
		print data
		error=""
		if(len(data) == 0):
			error = "No Books Found"
		return render_template("findbook.html",result = data, error=error)

''' Adding, Editing and Deleting a request'''
@app.route('/request_add', methods=['GET','POST'])
def addRequest():
	req = request.form["request"]
	conn = mysql.connect()
	cursor = conn.cursor()
	print req
	query = "INSERT INTO requests(user_id,requests,time_added) " \
			"VALUES(%s,%s,%s)"
	data = (session['ID'],req,time.strftime('%Y-%m-%d'))
	cursor.execute(query,data)
	conn.commit()
	return viewRequest()

@app.route('/view_request', methods=['GET','POST'])
def viewRequest():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT users.Name, users.email,users.number,requests.requests,requests.time_added from users,requests where users.ID = requests.user_id order by time_added DESC;")
	data = cursor.fetchall()
	# print data
	return render_template("view.html", result = data)


@app.route('/myRequest', methods=['GET','POST'])
def myRequest():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT requests.requests,requests.time_added from requests where requests.user_id='"+str(session['ID'])+"' order by time_added DESC;")
	data = cursor.fetchall()
	return render_template("myrequest.html", result = data)

@app.route('/editmyrequest',methods=['GET', 'POST'])
def editMyRquests():
	oreq = request.form["oldrequest"]
	req = request.form["request"]

	conn = mysql.connect()
	cursor =conn.cursor()
	cursor.execute("UPDATE requests set requests='"+req+"',time_added='"+time.strftime('%Y-%m-%d')+"'where requests='"+oreq+"'")
	conn.commit()

	return myRequest()


@app.route('/delmyrequest',methods=['GET', 'POST'])
def deleteRequests():
	req = request.form["request"]
	conn = mysql.connect()
	cursor =conn.cursor()
	cursor.execute("DELETE from requests where requests='"+req+"'")
	conn.commit()
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
	password = sha256_crypt.encrypt(password)
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
	cursor.execute("SELECT * from users where username='" + username +"'")
	data = cursor.fetchone()
	print data;
	if data is None:
		session["logged_in"]=False
		error = 'Username or Password Wrong!'
		return render_template('signin.html',error=error)
	elif(sha256_crypt.verify(password,data[3])):
		session['logged_in'] = True
		session['ID'] = data[0]
		session['username'] = username
		return home()
	else:
		error = 'Username or Password Wrong!'
		return render_template('signin.html',error=error)


@app.route("/logout")
def logout():
	session['logged_in'] = False
	return home()
	
if __name__ == '__main__':
	logging.basicConfig(filename='server.log',level=logging.DEBUG)
	app.run(debug = True,host= '0.0.0.0')

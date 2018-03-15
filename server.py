from flask import Flask, flash, redirect, render_template, request, session, abort
from flaskext.mysql import MySQL
import os

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Shayaan7'
app.config['MYSQL_DATABASE_DB'] = 'devops'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# @app.route('/')
# def student():
# 	return render_template('index.html')
# session["logged_in"]=False

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		return render_template("home.html")


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
		return home()

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return home()
	
if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug = True,host= '0.0.0.0')
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def student():
	return render_template('index.html')

@app.route('/about')
def hello():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug = True,host= '0.0.0.0')
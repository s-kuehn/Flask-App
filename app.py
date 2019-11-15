from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'home page'

@app.route('/contact')
def contact():
	return 'contact page'

@app.route('/about')
def about():
	return 'about page'
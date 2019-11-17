from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/send', methods=['POST'])
def send(sum=sum):
	if request.method == 'POST':
		cost = request.form['cost']
		revenue = request.form['revenue']
		print(cost)

		sum = float(cost) + float(revenue)
		return render_template('index.html', sum=sum)

@app.route('/contact')
def contact():
	return 'contact page'

@app.route('/about')
def about():
	return 'about page'
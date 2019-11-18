from flask import Flask, render_template, request, send_from_directory
import config
import csv
import os

app = Flask(__name__)

# Initialize Variables
margin = 0
cost = 0
revenue = 0
name = ''
filename = 'margins.csv'

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def send(sum=sum, margin=margin, cost=cost, revenue=revenue):
	if request.method == 'POST':

		# Get variables from input form
		name = request.form['name']
		cost = request.form['cost']
		revenue = request.form['revenue']

		# Calculate profit
		sum = '$' + str(round(float(revenue) - float(cost)))

		# Calculate margin
		percent = round(abs(float(cost) / float(revenue) - 1) * 100, 2)
		margin = str(percent) + '%'

		# Write to csv
		with open('data/margins.csv', 'a+', newline='') as csvfile:
			newdata = csv.writer(csvfile)
			newdata.writerow([name, cost, revenue, sum, margin])

		# Return answers
		return render_template('index.html',name=name, sum=sum, margin=margin, cost='$'+cost, revenue='$'+revenue)

# Download CSV file
@app.route('/data', methods=['POST', 'GET'])
def file():
	return send_from_directory('data/', "margins.csv")
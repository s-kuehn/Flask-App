from flask import Flask, render_template, request, send_from_directory, redirect
# from flask_sqlalchemy import SQLAlchemy
# import csv
# import os
import sqlite3

app = Flask(__name__)

# Initialize Variables
margin = 0
cost = 0
revenue = 0
product = ''
filename = 'margins.csv'

@app.route('/', methods=["GET", "POST"])
def home():
	if request.form:
		try:
			# Initialize variables
			product = request.form['product']
			cost = request.form['cost']
			revenue = request.form['revenue']
			sum = str(round(float(revenue) - float(cost), 2))
			percent = round(abs(float(cost) / float(revenue) - 1) * 100, 2)
			margin = str(percent)

			# Add row to database
			conn = sqlite3.connect('calculations.db')
			c = conn.cursor()
			c.execute("INSERT INTO calc(product, cost, revenue, profit, margin) VALUES('name', "+str(cost)+", "+str(revenue)+", "+str(sum)+", "+str(margin)+")")
			conn.commit()
			conn.close()
		except:
			print('not loading')

	# List all items from database
	conn = sqlite3.connect('calculations.db')
	c = conn.cursor()

	c.execute("""CREATE TABLE IF NOT EXISTS calc (
				id INTEGER PRIMARY KEY,
				product text,
				cost integer,
				revenue integer,
				profit integer,
				margin integer)""")

	c.execute("SELECT * FROM calc")
	items = c.fetchall()
	for item in items:
		print(item)
	conn.commit()
	conn.close()

	# Load Page
	return render_template('index.html', items=items)

@app.route('/delete', methods=['POST', 'GET'])
def deleteRow():
	pin = request.args.get('id')
	print(pin)
	conn = sqlite3.connect('calculations.db')
	c = conn.cursor()

	c.execute("DELETE FROM calc WHERE id="+pin+"")
	conn.commit()
	conn.close()
	return redirect('/')

# Download CSV file
@app.route('/data', methods=['POST', 'GET'])
def file():
	return send_from_directory('data/', "margins.csv")

@app.route('/clear', methods=['POST', 'GET'])
def clearTable():
	return render_template('index.html', items=items)


from flask import Flask, render_template, request, send_from_directory, redirect
import csv
import os
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
		# try:
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
		c.execute("INSERT INTO calc(product, cost, revenue, profit, margin) VALUES("+"'"+product+"'"+", "+str(cost)+", "+str(revenue)+", "+str(sum)+", "+str(margin)+")")
		conn.commit()
		conn.close()
		# except:
		# 	print('not loading')

	# List all items from database
	conn = sqlite3.connect('calculations.db')
	c = conn.cursor()

	c.execute("""CREATE TABLE IF NOT EXISTS calc (
				id INTEGER PRIMARY KEY,
				product TEXT,
				cost INTEGER,
				revenue INTEGER,
				profit INTEGER,
				margin INTEGER)""")

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
	# print(pin)
	conn = sqlite3.connect('calculations.db')
	c = conn.cursor()

	c.execute("DELETE FROM calc WHERE id="+pin+"")
	conn.commit()
	conn.close()
	return redirect('/')

# Download CSV file
@app.route('/data', methods=['POST', 'GET'])
def file():
	# Delete old csv file
	os.system('rm data/margins.csv')
	# Create and open csv file
	with open('data/margins.csv', 'a+') as f:
		writer =csv.writer(f)
		# Add header to file
		writer.writerow(['Name', 'Cost', 'Revenue', 'Profit', 'Margin'])
		# Connect to sqlite database
		conn = sqlite3.connect('calculations.db')
		c = conn.cursor()
		c.execute("SELECT * FROM calc")
		items = c.fetchall()
		# Write db items to csv file
		for item in items:
			writer.writerow([item[1], '$' + str(item[2]), '$' + str(item[3]),
				'$' + str(item[4]), str(item[5]) + '%'])
		conn.commit()
		conn.close()
	return send_from_directory('data/', "margins.csv")

@app.route('/clear', methods=['POST', 'GET'])
def clearTable():
	return render_template('index.html', items=items)


from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize Variables
margin = 0
cost = 0
revenue = 0

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/send', methods=['POST'])
def send(sum=sum, margin=margin, cost=cost, revenue=revenue):
	if request.method == 'POST':

		# Get variables from input form
		cost = request.form['cost']
		revenue = request.form['revenue']

		# Calculate profit
		sum = '$' + str(round(float(revenue) - float(cost)))

		# Calculate margin
		percent = round(abs(float(cost) / float(revenue) - 1) * 100, 2)
		margin = str(percent) + '%'

		# Return answers
		return render_template('index.html', sum=sum, margin=margin, cost='$'+cost, revenue='$'+revenue)

@app.route('/contact')
def contact():
	return 'contact page'

@app.route('/about')
def about():
	return 'about page'
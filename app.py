from functools import wraps
import os

from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from dbHandler import DBHandler
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')

db_handler = DBHandler(host="dpg-ci2aokak728i8t8mp4gg-a.oregon-postgres.render.com", port=5432, dbname="naamanins", user="naaman", password='EOeDYpXWHy88yJKnILlZlBe2IeUqdoCi')
db_handler.connect()
logged_in_users = {}
with open("config/Valid_users.json", "r") as data:
     valid_users = json.load(data)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or session['email'] not in logged_in_users:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session or perform any necessary logout operations
    logged_in_users[session['email']] = False
    session.clear()

    return redirect(url_for('login'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']

    # Perform authentication logic here
    # Check if email and password are valid
    # For now, let's assume any email and password is valid
    if email in valid_users["valid_emails"] and password:
        session['email'] = email
        logged_in_users[email] = True
        return redirect(url_for('client', email=email))
    else:
        error = "Invalid email or password"
        return render_template('login.html', error=error)


@app.route('/client/<email>')
@login_required
def client(email):
    print("email = ", email)
    if not (email in logged_in_users and logged_in_users[email]):
        return redirect(url_for('login'))
    email = session.get('email')

    # Check if the user is logged in
    if not email or email not in logged_in_users:
        return redirect(url_for('login'))

    return render_template('client.html', email=email)

@app.route('/get_sales_total', methods=['GET'])
@login_required

def get_sales_total():
    email = session.get('email')

    # Perform the database query to get the sum of prices for the email
    # Replace with your database query logic
    sum_price = db_handler.sum_sales_per_email(email)
    print(sum_price)

    # Return the sum of prices in JSON format
    return jsonify({'sumPrice': sum_price})

@app.route('/submit_data', methods=['POST'])
@login_required
def submit_data():
    print("here")
    id = request.form.get("id")
    name = request.form.get("name")
    price = request.form.get("price")
    insurance_type = request.form.get("insurance_type")
    email = session["email"]
    print(id, name, price, insurance_type)

    db_handler.insert_data(id, name, price, insurance_type,email)

    # Store the data in the database
    # Perform database operations here

    # For now, let's assume the data is successfully stored
    success_message = "Data submitted successfully"
    session['success_message'] = success_message

    return redirect(url_for('show_success_message'))


@app.route('/show_success_message')
@login_required
def show_success_message():
    success_message = session.pop('success_message', None)
    email = session.get('email')

    return render_template('client.html', email=email, success_message=success_message)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000)

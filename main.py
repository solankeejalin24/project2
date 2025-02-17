from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users = {}

def count_words(text):
    words = text.split()
    return len(words)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        address = request.form['address']

        # Check if username is already taken
        if username in users:
            error_message = "Username already exists. Choose a different one."
        else:
            # Store user information in the dictionary
            users[username] = {
                'password': password,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'address': address
            }

    return render_template('register.html', error_message=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password match
        user_info = users.get(username, None)
        if user_info and user_info['password'] == password:
            return render_template('success.html', user_info=user_info)
        else:
            error_message = "Username or password incorrect."

    return render_template('login.html', error_message=error_message)

@app.route('/success_register')
def success_register():
    username = request.args.get('username')
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    email = request.args.get('email')

    user_info = users.get(username, None)
    word_count = user_info.get('word_count', 0)

    return render_template('success_register.html', username=username, firstname=firstname, lastname=lastname, email=email, word_count=word_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
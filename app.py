from flask import Flask, request, render_template, session, g, abort, redirect, url_for
from config_key import configureFlaskSecretKey
from flask_bcrypt import Bcrypt #pip install flask-bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

configureFlaskSecretKey(app) #set our settings for flask

@app.route('/')
def index():
    #return 'Hello, World!'
    if is_logged_in():
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

@app.route('/register')
def register():
    if request.method == 'POST':
            #do registration
            if validate_registration(request.form['username'], 
                request.form['password'],
                request.form['confirmpassword'],
                request.form['email']):
                register_user(request.form['username'], request.form['password'], request.form['email'])
                return redirect(url_for('login'))
            else:
                error = "Invalid information."
                return render_template('register.html', error=error)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #do login
        if validate_login(request.form['username'],
                       request.form['password']):
            return do_login(request.form['username'])
        else:
            error = 'Invalid username/password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.errorhandler(404)
def page_not_found(error):
    return "We  didn't think it be like it was but it do. We can't find that page!", 404


def is_logged_in():
    return 'username' in session

def validate_login(username, password):
    #validate if password for the username is correct
    pw_hash = '' #get from database
    #bcrypt.check_password_hash(pw_hash, password)
    return True

def do_login(username):
    session['username'] = username
    return redirect(url_for('dashboard')) #redirect to dashboard

@app.route('/logout')
def do_logoff():
    if is_logged_in():
         session.pop('username', None)
    return redirect(url_for('index'))

def validate_registration(username, password, confirmpassword, email):
    return True

def register_user(username, password, email):
    pw_hash = bcrypt.generate_password_hash(password)
    pass

if __name__ == "__main__":
    app.run()
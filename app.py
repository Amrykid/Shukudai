from flask import Flask, request, render_template, session, g, abort, redirect, url_for
from config_key import configureFlaskSecretKey
from database import configure_database_flask, create_user, get_user, add_user
from flask_bcrypt import Bcrypt #pip install flask-bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

configureFlaskSecretKey(app) #set our settings for flask

#todo, make an actual database
#based on tutorial here: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
#and here http://flask-sqlalchemy.pocoo.org/2.3/quickstart/#a-minimal-application
configure_database_flask(app)

@app.route('/')
def index():
    #return 'Hello, World!'
    if is_logged_in():
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            #do registration
            result, error = validate_registration(request.form['username'], 
                request.form['password'],
                request.form['confirmpassword'],
                request.form['email'])

            if result:
                register_user(request.form['username'], request.form['password'], request.form['email'])
                return redirect(url_for('login'))
            else:
                return render_template('register.html', error=error)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in(): return redirect(url_for("dashboard"))

    if request.method == 'POST':
        #do login
        result, error = validate_login(request.form['username'],
                       request.form['password'])
        if result:
            return do_login(request.form['username'])
        else:
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not is_logged_in(): return redirect(url_for("login"))

    return render_template('dashboard.html', username=session['username'])

@app.errorhandler(404)
def page_not_found(error):
    return "We  didn't think it be like it was but it do. We can't find that page!", 404


def is_logged_in():
    return 'username' in session

def validate_login(username, password):
    #validate if password for the username is correct
    user = get_user(username)
    if user == None: return (False, "Invalid username")

    pw_hash = user.password #get from database
    result = bcrypt.check_password_hash(pw_hash, password)

    if result: return (True, "")
    else: return (False, "Invalid username or password") #make it ambiguous

def do_login(username):
    session['username'] = username
    return redirect(url_for('dashboard')) #redirect to dashboard

@app.route('/logout')
def do_logoff():
    if is_logged_in():
         session.pop('username', None)
    return redirect(url_for('index'))

def validate_registration(username, password, confirmpassword, email):
    existing_user = get_user(username)

    if existing_user is not None:
        return (False, "Username already exists!")

    if confirmpassword != password:
        return (False, "Both passwords entered do not match!")

    #todo validate email address correctly
    if email.count('@') == 0:
        return (False, "Email address is not correct.")

    return (True, None) #the light is green

    #todo at some point, we should sent the user an email

def register_user(username, password, email):
    pw_hash = bcrypt.generate_password_hash(password)

    usr = create_user(username=username,password=pw_hash,email=email)
    add_user(usr)

if __name__ == "__main__":
    app.run()
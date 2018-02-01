from flask import Flask, request, render_template, session, g, abort, redirect, url_for
from config_key import configureFlaskSecretKey
app = Flask(__name__)

configureFlaskSecretKey(app) #set our settings for flask

@app.route('/')
def index():
    #return 'Hello, World!'
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return "We  didn't think it be like it was but it do. We can't find that page!", 404


if __name__ == "__main__":
    app.run()
#pip install sqlalchemy
#pip install flask-sqlalchemy
#from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UserObj = None

db = None

def configure_database_flask(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(18), nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username

    db.create_all()

    UserObj = User

def create_user(username, email, password):
    return UserObj(usernam=username, email=email, password=password)

def get_user(username):
    return UserObj.query.filter_by(username=username).first()
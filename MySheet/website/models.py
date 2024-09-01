from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    email_v = db.Column(db.Integer)

class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    owner_id = db.Column(db.Integer)

class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sheet_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    access_type = db.Column(db.Integer) #0-->editor  1-->viewer



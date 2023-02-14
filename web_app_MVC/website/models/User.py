from website.config import db
from flask_login import UserMixin
from website.models.Routine import Routine

class User(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    routine = db.relationship('Routine', backref = 'user', uselist = False)
from website.config import db

class Yogapose(db.Model):
        
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    exercises= db.relationship('Exercise', backref='yogapose')
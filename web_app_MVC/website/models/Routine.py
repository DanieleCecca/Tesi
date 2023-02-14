from website.config import db
from website.models.Exercise import Exercise, routine_exercise

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    playing = db.relationship('Exercise', secondary=routine_exercise, backref = 'routine')
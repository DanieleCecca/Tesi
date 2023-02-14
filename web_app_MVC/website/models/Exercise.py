from website.config import db


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=id)
    yogapose_id=db.Column(db.Integer, db.ForeignKey('yogapose.id')) 


routine_exercise= db.Table('routine_exercise',
                           db.Column('routine_id', db.Integer, db.ForeignKey('routine.id')),
                           db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id')))
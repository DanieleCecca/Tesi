from flask import Blueprint, render_template,request,flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from website.config import db
from website.models.Routine import Routine
from website.models.YogaPose import Yogapose
from website.models.Exercise import Exercise
import json

routine = Blueprint('routine', __name__)


@routine.route('/create-routine', methods=['GET', 'POST'])
@login_required
def create_routine():
    exercises_list_name=[]
    exercises_list=[]
    routine = Routine()
    if request.method == 'POST':
        exercise = request.form.get('exercise')#get the id of exercise dal form ossia della yogapose
        if not exercise:
            flash('Select at least one exercise!', category='error')
        else:
            pose = Yogapose.query.filter_by(id = exercise).first() # accedo al database
            new_exercise = Exercise(yogapose_id = pose.id)
            db.session.add(new_exercise)
            db.session.commit()
            if current_user.routine == None:
                routine = Routine(user_id=current_user.id)
                routine.playing.append(new_exercise)
                db.session.commit()
            else:
                routine = Routine.query.filter_by(user_id = current_user.id).first()
                routine.playing.append(new_exercise)
                db.session.commit()
    
    #script per gli elemnti nell'html
    yoga_poses = db.session.query(Yogapose).all()
    for exercise in routine.playing:
        exercises_list.append(Exercise.query.filter_by(id = exercise.id).first())
        exercises_list_name.append(Yogapose.query.filter_by(id = exercise.yogapose_id).first())
    return render_template("routines.html", user=current_user, yoga_poses=yoga_poses, exercises_list = exercises_list,exercises_list_name= exercises_list_name,zip=zip)
    
    
@routine.route('/delete-exercise', methods=['POST'])
def delete_exercise():
    exercise = json.loads(request.data)
    print(exercise)
    exercise_id = exercise['exercise_id']
    print(exercise_id)
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        db.session.delete(exercise)
        db.session.commit()

    return jsonify({})
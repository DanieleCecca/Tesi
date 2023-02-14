from flask import Blueprint, jsonify, render_template,Response,current_app, url_for
from flask_login import login_required,current_user
import cv2

from website.config import db
from ..utils.constants import *
from website.controllers.Movenet import Movenet
from website.controllers.Classificator import Classificator
from website.controllers.Checker import Checker
from website.models.YogaPose import Yogapose
from website.models.Routine import Routine
from website.models.Timer import Timer

import ast




import numpy as np

movenet_model = Movenet()
rnn_model = Classificator()
checker = Checker()
timer = Timer()
videoStreaming= Blueprint('videoStreaming', __name__)




def gen_frames_free():
    sequence=[]
    predictions=[]
    posa='nessuno'
    camera = cv2.VideoCapture(2)
    dataset_posa= None
    stringa = ''

    image_height, image_width = [480,640]
    print(image_height, image_width)
    crop_region = movenet_model.init_crop_region(image_height, image_width)
    
    while True:
        ret, frame = camera.read() 
        if not ret:
            break
        else:
            ret,frame = camera.read()
            #image = frame
            keypoints_with_scores = movenet_model.run_inference(
            movenet_model.movenet, frame, crop_region,
            crop_size=[256, 256])

            crop_region = movenet_model.determine_crop_region(
            keypoints_with_scores, image_height, image_width)
            movenet_model.draw_skeleton(frame, keypoints_with_scores, 0.3)

            #predict logic 
            keypoint = movenet_model.extract_keypoints(keypoints_with_scores)
            sequence.append(keypoint)
            sequence= sequence[-45:]

            if len(sequence)==45:
                res = rnn_model.model.predict(np.expand_dims(sequence,axis=0))[0]
                predictions.append(np.argmax(res))

                #scrivere su schermo la scritta
                if np.unique(predictions[-10:])[0]==np.argmax(res):# controlla che le ultime 10 predizioni siano uguali
                    if res[np.argmax(res)] > 0.3:
                        posa = actions[np.argmax(res)]
                        dataset_posa = eval('checker.dataset_'+ posa)

                
                frame = rnn_model.prob_viz(res,actions, frame)

            cv2.rectangle(frame, (0,0), (640,40), (245,117,16), -1)
            cv2.putText(frame, posa, (3,30), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2, cv2.LINE_AA)
            
            if posa != 'nessuno':
                angl_vid=checker.knn_angoli(1,dataset_posa,keypoint)


                keypoint = keypoint.reshape((17,3))      
                angl_u=checker.calculate_all_angles(keypoint)

                frame = checker.draw_angles(angl_u,frame)
                
                checker.correct_angles(20,angl_vid,angl_u,posa)
                


            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            


def gen_frames_routine(exercises_list):
    sequence=[]
    predictions=[]
    camera = cv2.VideoCapture(2)
    #with current_app.app_context():
     #   routine = Routine.query.filter_by(user_id = current_user.id).first()
    #for exercise in routine.playing:
     #   exercises_list.append(Yogapose.query.filter_by(id = exercise.id)).name
    
    #poichè per qualche motivo ho una stringa e non una lista trasformo la stringa in lista es '['','']'->['','']
    print(exercises_list)
    exercises_list = ast.literal_eval(exercises_list)
    posa = exercises_list[0]
    dataset_posa=eval('checker.dataset_'+ posa)


    image_height, image_width = [480,640]
    print(image_height, image_width)
    crop_region = movenet_model.init_crop_region(image_height, image_width)
    if(timer.get_time()>30 and timer._start_time!= 0):
        timer.stop()
    timer.start()
    i=0
    while True:
        ret, frame = camera.read() 
        if not ret:
            break
        else:
            ret,frame = camera.read()
            #image = frame

            keypoints_with_scores = movenet_model.run_inference(
            movenet_model.movenet, frame, crop_region,
            crop_size=[256, 256])

            crop_region = movenet_model.determine_crop_region(
            keypoints_with_scores, image_height, image_width)
            movenet_model.draw_skeleton(frame, keypoints_with_scores, 0.3)

            #predict logic 
            keypoint = movenet_model.extract_keypoints(keypoints_with_scores)
            sequence.append(keypoint)
            #sequence= sequence[-45:]

            
            #impostare un timer
            #print(len(sequence))
            if timer.get_time()==30: # ogni 30 sec cambia posizione 
                i+=1
                if i >= len(exercises_list):
                    break #usare url for
                posa=exercises_list[i]
                dataset_posa = eval('checker.dataset_'+ posa)
                timer.stop()
                timer.start()
             
            

            cv2.rectangle(frame, (0,0), (640,40), (245,117,16), -1)
            cv2.putText(frame, posa, (3,30), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2, cv2.LINE_AA)
            
            angl_vid=checker.knn_angoli(1,dataset_posa,keypoint)


            keypoint = keypoint.reshape((17,3))      
            angl_u=checker.calculate_all_angles(keypoint)

            frame = checker.draw_angles(angl_u,frame)
                
            checker.correct_angles(20,angl_vid,angl_u,posa)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return
            

@videoStreaming.route('/free-video',methods=['GET', 'POST'])
@login_required
def free_video():
    flag = 1
    stringa= rnn_model.get_stringa()
    print(stringa)
    return render_template('Streaming.html', user=current_user, flag = flag, stringa = stringa)  

@videoStreaming.route('/free-video-streaming',methods=['GET', 'POST'])
@login_required
def define_free_videoStreaming():
        return Response(gen_frames_free(), mimetype='multipart/x-mixed-replace; boundary=frame')
   
 
@videoStreaming.route('/routine-video',methods=['GET', 'POST'])
@login_required
def routine_video():
    flag = 0
    routine = Routine.query.filter_by(user_id = current_user.id).first()
    print(routine.playing)
    exercises_list=[]
    for exercise in routine.playing:
        exercises_list.append(Yogapose.query.filter_by(id = exercise.yogapose_id).first().name)
    return render_template('Streaming.html', user=current_user, flag =flag, exercises_list = exercises_list)  

@videoStreaming.route('/routine-video-streaming/<exercises_list>',methods=['GET', 'POST'])
@login_required
def define_routine_videoStreaming(exercises_list):
    print(exercises_list)
    return Response(gen_frames_routine(exercises_list), mimetype='multipart/x-mixed-replace; boundary=frame')

@videoStreaming.route('/rendering-correction',methods=['GET', 'POST'])
@login_required
def render_correction():
    return jsonify(correction = checker.get_stringa())

@videoStreaming.route('/rendering-prob',methods=['GET', 'POST'])
@login_required
def render_prob():
    return jsonify(prob = rnn_model.get_stringa())

@videoStreaming.route('/rendering-timer',methods=['GET', 'POST'])
@login_required
def render_timer():
    if timer._start_time==0:#fare funzione get
        time = 0
    else:
        time= timer.get_time()
    return jsonify(timer = str(time))

    
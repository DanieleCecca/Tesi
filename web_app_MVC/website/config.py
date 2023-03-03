from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import sys
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok

db= SQLAlchemy()
DB_NAME = "database.db"

port_no =5000


def create_app():
    
    #Inizializziamo un oggetto di tipo Flask
    app = Flask(__name__,template_folder='views')
    
    ngrok.set_auth_token("2MSD7Ew2kcpKaT3R1N0RtC11OF7_3v2pbuSEFJdCRJjzYWBqY")
    public_url = ngrok.connect(port_no).public_url
    print(public_url)

    
    
    #DATABASE Section
    app.config['SECRET_KEY']= 'chiave segreta'
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    
    #devono andare per forza qui
    from website.controllers.routes.auth_routes import auth
    from website.controllers.routes.views_routes import views
    from website.controllers.routes.routines_routes import routine
    from website.controllers.routes.video_routes import videoStreaming
    
    from website.models.User import User
    from website.models.Routine import Routine
    from website.models.YogaPose import Yogapose  
    from website.models.Exercise import Exercise
    from website.models.Exercise import routine_exercise
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
       
    
    #LOGIN MANAGER section
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'#dove ci reindirizza  se non siamo loggati
    login_manager.init_app(app) #inizializziamo il login manager con app
       
    
    #ROUTES/BLUEPRINT section
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(routine, url_prefix='/')
    app.register_blueprint(videoStreaming, url_prefix='/')
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    
    with app.app_context():
        db.session.add_all([
        Yogapose(name='Corpse'),
        Yogapose(name='Cobra'),
        Yogapose(name='Lotus'),
        Yogapose(name='Mountain'),
        Yogapose(name='Tree'),
        Yogapose(name='Triangle')])
        db.session.commit()
    
        
    return app
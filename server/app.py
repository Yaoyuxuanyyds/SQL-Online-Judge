from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os,sys
sys.path.append(os.getcwd())
import config
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from resources import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    api = Api(app)
    
    @app.route('/')
    def h():
        return ''

    # 注册资源API
    api.add_resource(Community, '/api/community')
    api.add_resource(CommunityList, '/api/communitylist')
    api.add_resource(Judge, '/api/judge')
    api.add_resource(Login, '/api/login')
    api.add_resource(ManageUsers, '/api/manageusers')
    api.add_resource(Question, '/api/question')
    api.add_resource(QuestionList, '/api/questionlist')  
    api.add_resource(Register, '/api/register')
    api.add_resource(Student, '/api/student')
    api.add_resource(StudentList, '/api/studentlist')
    api.add_resource(Submit, '/api/submit')
    api.add_resource(SubmitList, '/api/submitlist')
    api.add_resource(ContestList, '/api/contestlist')
    api.add_resource(Contest, '/api/contest')


    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
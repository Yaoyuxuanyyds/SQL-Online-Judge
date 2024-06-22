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
    CORS(app, resources={r"/*": {"origins": "*"}})  # 允许所有来源的请求
    
    api = Api(app)
    
    @app.route('/')
    def h():
        return ''

    # 注册资源API
    api.add_resource(QuestionList, '/api/questionlist')  # 注册题目列表API
    api.add_resource(Register, '/api/register')
    api.add_resource(Questions, '/api/questions/<int:question_id>')
    api.add_resource(Login, '/api/login')
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
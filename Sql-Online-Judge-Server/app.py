from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os,sys
sys.path.append(os.getcwd())
from exts import db
from resources.question import QuestionList, Questions
from resources.register import Register

import config
from auth import auth  # 导入新的身份验证蓝图

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})  # 允许所有来源的请求
    
    api = Api(app)
    
    @app.route('/')
    def hello_world():
        return 'Hello World!'

    # 注册蓝图
    app.register_blueprint(auth)

    # 注册资源API
    api.add_resource(QuestionList, '/api/questionlist')  # 注册题目列表API
    api.add_resource(Register, '/api/reguester')
    api.add_resource(Questions, '/api/questions/<int:question_id>')

    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

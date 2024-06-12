from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os,sys
sys.path.append(os.getcwd())
from exts import db
from resources.students import StudentList, Students
from resources.question import QuestionList, Questions
from resources.answer import AnswerList, Answers
from resources.submit import SubmitList, Submits
from resources.register import Register
import config
from auth import auth  # 导入新的身份验证蓝图

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    CORS(app)
    
    api = Api(app, errors=config.errors)
    
    @app.route('/home')
    def hello_world():
        return 'Hello World!'

    # 注册蓝图
    app.register_blueprint(auth)

    # 添加资源路由
    api.add_resource(Students, '/student/<string:student_id>')
    api.add_resource(StudentList, '/student')
    api.add_resource(Questions, '/question/<int:question_id>')
    api.add_resource(QuestionList, '/question')
    api.add_resource(Answers, '/question/<int:idQuestion>/answer/<int:answer_id>')
    api.add_resource(AnswerList, '/question/<int:idQuestion>/answer')
    api.add_resource(Submits, '/student/<int:idStudent>/submit/<int:submit_id>')
    api.add_resource(SubmitList, '/submit', '/question/<int:idQuestion>/submit',
                     '/question/<int:idQuestion>/student/<int:idStudent>/submit')
    api.add_resource(Register, '/register')

    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

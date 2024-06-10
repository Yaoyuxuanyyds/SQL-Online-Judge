from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import sys,os
sys.path.append(os.getcwd())
from exts import db
from resources.adminSession import AdminSession
from resources.studentSession import StudentSession
from resources.teacherSession import TeacherSession  # 新增老师登录资源
from resources.schemas import Schema, SchemaList
from resources.table import Table, TableList
from resources.rows import Rows, RowsList
from resources.students import StudentList, Students
from resources.question import QuestionList, Questions
from resources.answer import AnswerList, Answers
from resources.segmentation import Segmentation, SegmentationList
from resources.submit import SubmitList, Submits
from resources.register import Register  # 导入注册资源
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    CORS(app)
    
    api = Api(app, errors=config.errors)
    
    @app.route('/')
    def hello_world():
        return 'Hello World!'

    # 添加资源路由
    api.add_resource(Students, '/student/<string:student_id>')
    api.add_resource(StudentList, '/student')
    api.add_resource(AdminSession, '/session/admin')
    api.add_resource(StudentSession, '/session/student')
    api.add_resource(TeacherSession, '/session/teacher')  # 添加老师登录资源
    api.add_resource(Schema, '/schema/<int:schema_id>')
    api.add_resource(SchemaList, '/schema')
    api.add_resource(Table, '/schema/<int:idSchema>/table/<int:table_id>')
    api.add_resource(TableList, '/schema/<int:idSchema>/table')
    api.add_resource(Rows, '/table/<int:idTable>/rows/<int:rows_id>')
    api.add_resource(RowsList, '/table/<int:idTable>/rows')
    api.add_resource(Questions, '/question/<int:question_id>')
    api.add_resource(QuestionList, '/question')
    api.add_resource(Answers, '/question/<int:idQuestion>/answer/<int:answer_id>')
    api.add_resource(AnswerList, '/question/<int:idQuestion>/answer')
    api.add_resource(Segmentation, '/answer/<int:idAnswer>/segment/<int:segmentation_id>')
    api.add_resource(SegmentationList, '/answer/<int:idAnswer>/segment')
    api.add_resource(Submits, '/student/<int:idStudent>/submit/<int:submit_id>')
    api.add_resource(SubmitList, '/submit', '/question/<int:idQuestion>/submit',
                     '/question/<int:idQuestion>/student/<int:idStudent>/submit')
    api.add_resource(Register, '/register')  # 添加注册资源路由

    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

# ws3917 - 数据库里面所有的表
from sqlalchemy import ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, FLOAT, TEXT, BOOLEAN
from exts import db
# 用户表
class User(db.Model):
    __tablename__ = 'User'
    # 用户id, 名字，密码，权限组，登录状态标识符
    id = db.Column(INTEGER, primary_key=True)
    username = db.Column(VARCHAR(50), unique=True, nullable=False)
    password = db.Column(VARCHAR(255), nullable=False)
    role = db.Column(INTEGER, nullable=False)
    session = db.Column(VARCHAR(255), nullable=True)
    
class Question(db.Model):
    __tablename__ = 'Question'
    # 题目id,名字，建表语句,题目描述，
    id = db.Column(INTEGER, primary_key=True)
    title = db.Column(VARCHAR(1000), nullable=False)
    create_code = db.Column(TEXT, nullable=False)
    description = db.Column(TEXT, nullable=False)
    output = db.Column(TEXT, nullable=False)
    difficulty = db.Column(INTEGER, nullable=False)
    answer_example = db.Column(TEXT, nullable=False)
    is_public = db.Column(BOOLEAN, nullable=False, default=True)

class Exam(db.Model):
    __tablename__ = 'Exam'

    id = db.Column(INTEGER, primary_key=True)
    teacher_id = db.Column(INTEGER, db.ForeignKey('User.id'))
    start_time = db.Column(TIMESTAMP, nullable=False)
    end_time = db.Column(TIMESTAMP, nullable=False)
    teacher = db.relationship('User', foreign_keys=[teacher_id])

class ExamQuestion(db.Model):
    __tablename__ = 'Exam_Question'

    exam_id = db.Column(INTEGER, db.ForeignKey('Exam.id'), primary_key=True)
    question_id = db.Column(INTEGER, db.ForeignKey('Question.id'), primary_key=True)
    score = db.Column(INTEGER, nullable=False, default=10)
    exam = db.relationship('Exam', foreign_keys=[exam_id])
    question = db.relationship('Question', foreign_keys=[question_id])

class ExamStudent(db.Model):
    __tablename__ = 'Exam_Student'

    exam_id = db.Column(INTEGER, db.ForeignKey('Exam.id'), primary_key=True)
    student_id = db.Column(INTEGER, db.ForeignKey('User.id'), primary_key=True)
    score = db.Column(INTEGER, nullable=False, default=0)
    exam = db.relationship('Exam', foreign_keys=[exam_id])
    student = db.relationship('User', foreign_keys=[student_id])

class TestCase(db.Model):
    __tablename__ = 'Test_Case'

    id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    question_id = db.Column(INTEGER, db.ForeignKey('Question.id'))
    input_sql = db.Column(VARCHAR(255), nullable=False)
    output = db.Column(VARCHAR(255), nullable=False)
    question = db.relationship('Question', foreign_keys=[question_id])

class Submission(db.Model):
    __tablename__ = 'Submission'

    id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    student_id = db.Column(INTEGER, db.ForeignKey('User.id'))
    exam_id = db.Column(INTEGER, db.ForeignKey('Exam.id'))
    question_id = db.Column(INTEGER, db.ForeignKey('Question.id'))
    submit_sql = db.Column(TEXT, nullable=False)
    submit_time = db.Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    pass_rate = db.Column(FLOAT, nullable=False)
    status = db.Column(INTEGER, nullable=False)
    student = db.relationship('User', foreign_keys=[student_id])
    exam = db.relationship('Exam', foreign_keys=[exam_id])
    question = db.relationship('Question', foreign_keys=[question_id])

class Article(db.Model):
    __tablename__ = 'Article'

    id = db.Column(INTEGER, primary_key=True)
    title = db.Column(VARCHAR(1000), nullable=False)
    user_id = db.Column(INTEGER, db.ForeignKey('User.id'))
    question_id = db.Column(INTEGER, db.ForeignKey('Question.id'))
    is_notice = db.Column(BOOLEAN, nullable=False)
    content = db.Column(TEXT, nullable=False)
    publish_time = db.Column(TIMESTAMP, nullable=False)
    last_modify_time = db.Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    user = db.relationship('User', foreign_keys=[user_id])
    question = db.relationship('Question', foreign_keys=[question_id])

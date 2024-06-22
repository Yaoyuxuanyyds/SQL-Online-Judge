from flask import request, jsonify
from flask_restful import Resource, fields, marshal_with, marshal
import models, time, hashlib, os
from app import db
from config import *
from permissions import auth_role
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, TimeoutError, OperationalError
from sqlalchemy.orm import sessionmaker

# answer
answer_field = {
    'id': fields.Integer,
    'idQuestion': fields.Integer,
    'sql': fields.String,
    'json': fields.String,
}

class Answers(Resource):
    @auth_role(3,False)
    @marshal_with(answer_field)
    def get(self, idQuestion, answer_id):
        ret = models.Answer.query.filter_by(id=answer_id).first()
        if ret:
            return ret, HTTP_OK
        else:
            return {"message": "该答案不存在"}, HTTP_NotFound

    @auth_role(2,False)
    def delete(self, idQuestion, answer_id):
        ret = models.Answer.query.filter_by(id=answer_id).first()
        if ret:
            question = ret.Question
            db.session.delete(ret)
            db.session.commit()
            answer_left = models.Answer.query.filter_by(idQuestion=question.id).first()
            if answer_left is None:
                question.result = None
                db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该答案不存在"}, HTTP_NotFound

class AnswerList(Resource):
    @auth_role(3,False)
    def get(self, idQuestion):
        answers = models.Answer.query.filter_by(idQuestion=idQuestion)
        data = [marshal(answer, answer_field) for answer in answers]
        return {'data': data}, HTTP_OK

    @auth_role(2,False)
    def post(self, idQuestion):
        answer = models.Answer()
        answer.idQuestion = idQuestion
        question = models.Question.query.get(answer.idQuestion)
        answer.sql = request.json.get('sql')    # 这里的sql是代码内容(code)
        if answer.sql is None:
            return {"message": "没提供答案，无法提交！"}, HTTP_Bad_Request
        if answer.idQuestion is None:
            return {"message": "指定答案对应的题目！"}, HTTP_Bad_Request
        if question is None:
            return {"message": "答案对应的题目不存在！"}, HTTP_Bad_Request

        db.session.add(answer)
        db.session.commit()

        return {}, HTTP_Created

# judge
# 定义返回结果的字段
submit_judge = {
    'submit_sql': fields.String,
    'question_id': fields.Integer
}

class SQLJudge(Resource):
    @auth_role(3)
    @marshal_with(submit_judge)
    def execute_sql(self, code):
        """
        运行SQL代码，并捕获可能的错误和异常
        :param code: 要执行的SQL代码
        :return: 执行结果，格式为 (error: bool, msg: str)
        """
        # 创建数据库引擎，连接到testdb数据库
        engine = create_engine('mysql+pymysql://test:4546@localhost/testdb')
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.begin()  # 开始事务
            start_time = time.time()  # 记录开始时间
            
            result = session.execute(text(code))  # 执行SQL代码
            session.commit()  # 提交事务

            if result.returns_rows:  # 如果返回结果
                output = result.fetchall()  # 获取所有结果
            else:
                output = None  # 如果没有返回结果，设置为None

            elapsed_time = time.time() - start_time  # 计算执行时间

            if elapsed_time > 5:  # 判断是否超时
                return (True, "TLE")  # 超时返回TLE

            return (False, str(output))  # 返回执行结果

        except OperationalError as e:  # 捕获操作错误异常
            session.rollback()  # 回滚事务
            return (True, str(e))  # 返回错误信息
        except TimeoutError:  # 捕获超时异常
            session.rollback()  # 回滚事务
            return (True, "TLE")  # 返回超时错误信息
        except SQLAlchemyError as e:  # 捕获SQLAlchemy异常
            session.rollback()  # 回滚事务
            return (True, str(e))  # 返回错误信息
        finally:
            session.close()  # 关闭会话

    def drop_tables(self, tablename):
        """
        删除指定的表，避免数据干扰
        :param tablename: 需要删除的表名（可能有多个表名，以逗号分隔）
        """
        # 创建数据库引擎，连接到testdb数据库
        engine = create_engine('mysql+pymysql://low_permission_user:password@localhost/testdb')
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.begin()  # 开始事务
            # 关闭外键检查
            session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            # 删除指定表
            session.execute(text(f'DROP TABLE IF EXISTS {tablename};'))
            # 重新打开外键检查
            session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            session.commit()  # 提交事务
        except SQLAlchemyError:  # 捕获SQLAlchemy异常
            session.rollback()  # 回滚事务
        finally:
            session.close()  # 关闭会话

    def judge(self, submit_sql, question_id):
        """
        根据question_id从测试用例表读取对应的input_sql和output_sql，执行用户提交的SQL语句并判断结果
        :param submit_sql: 用户提交的SQL语句
        :param question_id: 问题ID
        :return: 测试结果字典，格式为 {测试用例ID: (error: bool, output: int)}
        """
        # 从TestCase表中获取对应question_id的所有测试用例
        test_cases = models.TestCase.query.filter_by(question_id=question_id).all()
        results = {}  # 存储测试结果的字典
        
        for test_case in test_cases:  # 遍历每个测试用例
            test_id = test_case.id  # 获取测试用例ID
            input_sql = test_case.input_sql  # 获取输入SQL
            expected_output = test_case.output  # 获取预期输出
            tablename = test_case.tablename  # 获取表名

            # 清理当前的表，避免表已存在造成干扰
            self.drop_tables(tablename)

            # 执行建表语句，初始化表结构
            error, setup_msg = self.execute_sql(input_sql)
            if error:  # 如果建表语句执行出错
                results[test_id] = (True, 1)  # 返回错误信息
                continue

            # 执行用户提交的SQL
            error, user_output = self.execute_sql(submit_sql)

            if error:  # 如果用户SQL执行出错
                if user_output == "TLE":  # 判断是否超时
                    results[test_id] = (True, 3)
                elif "MemoryError" in user_output:  # 判断是否内存溢出
                    results[test_id] = (True, 4)
                else:  # 其他错误
                    results[test_id] = (True, 1)
            elif user_output != expected_output:  # 判断输出是否正确
                results[test_id] = (True, 2)  # 输出错误
            else:
                results[test_id] = (False, 0)  # 正确通过

        return results  # 返回测试结果

# login
class Login(Resource):
    def post(self):
        user_id = request.json.get('id')
        password = request.json.get('password')
        user = models.User.query.filter_by(id=user_id, password=hashlib.sha256(password.encode('utf8')).hexdigest()).first()

        if user:
            session_token = hashlib.sha1(os.urandom(24)).hexdigest()
            user.session = session_token
            db.session.commit()
            return {"session": session_token, 
                    "role": user.role, 
                    "name": user.username}, HTTP_OK
        else:
            return {"message": '用户名或密码无效'}, HTTP_Unauthorized
        
    def logout(self):
        session = request.json.get('session')
        user = models.User.query.filter_by(session=session).first()
        if user:
            user.session = None
            db.session.commit()
            return {"message": '成功退出登录'}, HTTP_OK
        else:
            return {"message": '身份信息无效！请重新登录。'}, HTTP_Unauthorized
        
    def get(self):
        session = request.headers.get('session')
        user = models.User.query.filter_by(session=session).first()
        if user:
            return {
                "id": user.id, 
                "name": user.username, 
                "role": user.role
            }, HTTP_OK
        else:
            return {"message": '身份信息无效！请重新登录。'}, HTTP_Unauthorized

# questions
question_field = {
    'id': fields.Integer,
    'title': fields.String,
    'create_code': fields.String,
    'description': fields.String,
    'difficulty': fields.Integer,
    'answer_example': fields.String
}

# 处理单个题目的相关功能
class Questions(Resource):
    @auth_role(3,False)
    @marshal_with(question_field)
    def get(self, question_id):
        # 查询单个题目 -> 用于题目查询和显示
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            return ret, HTTP_OK
        else:
            return {"message": "该题目不存在"}, HTTP_NotFound

    @auth_role(2,False)
    def delete(self, question_id):
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该题目不存在"}, HTTP_NotFound
    
    @auth_role(2, False)
    def post(self):
        q = models.Question()
        q.title = request.json['title']
        q.description = request.json['description']
        q.difficulty = request.json['difficulty']
        q.answer_example = request.json['answer_example']
        if q.title is None or q.description is None or q.difficulty is None or q.answer_example is None:
            return {"message": "题目信息不全，补全缺失项！"}, HTTP_Bad_Request
        db.session.add(q)
        db.session.commit()
        return {"message": "新增题目成功"}, HTTP_Created

# 处理题目列表的相关功能
class QuestionList(Resource):
    @auth_role(3, inject=False)
    def get(self):
        # 查询所有题目 -> 用于题目列表的查询和显示
        questions = models.Question.query.all()
        data = [marshal(q, question_field) for q in questions]
        return {'data': data}, HTTP_OK

# register
class Register(Resource):
    def post(self):
        id = request.json.get('id', None)
        username = request.json.get('username', None)
        password = hashlib.sha256(request.json.get('password', 0).encode('utf8')).hexdigest() 
        
        if models.User.query.filter_by(id=id).first():
            return {"message": "ID撞车了，换一个。"}, HTTP_Conflict
        if models.User.query.filter_by(username=username).first():
            return {"message": "有人跟你重名了，换一个。"}, HTTP_Conflict
        
        new_user = models.User(id=id, username=username, password=password, role=0)  # 默认角色为0
        db.session.add(new_user)
        db.session.commit()
        return {"message": "成了，快去登录吧！"}, HTTP_Created

# students
student_fields = {
    'id': fields.String,
    'name': fields.String,
    'password': fields.String
}

class Students(Resource):
    method_decorators = [auth_role(2, False)]

    @marshal_with(student_fields)
    def get(self, student_id):
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            return ret, HTTP_OK
        else:
            return {"message": "该学生不存在"}, HTTP_NotFound

    def delete(self, student_id):
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该学生不存在"}, HTTP_NotFound

    def put(self, student_id):
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            ret.password = request.json['password']
            ret.name = request.json['username']
            try:
                db.session.commit()
            except Exception as e:
                return {"message": f"错误：{str(e)}"}, HTTP_Bad_Request
            return {}, HTTP_OK
        else:
            return {"message": "该学生不存在"}, HTTP_NotFound

    def patch(self, student_id):
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            ret.password = ret.password if request.json['password'] is None else request.json['password']
            ret.name = ret.name if request.json['username'] is None else request.json['username']
            try:
                db.session.commit()
            except Exception as e:
                return {"message": f"错误：{str(e)}"}, HTTP_Bad_Request
            return {}, HTTP_OK
        else:
            return {"message": "该学生不存在"}, HTTP_NotFound

class StudentList(Resource):
    method_decorators = []

    @auth_role(2, False)
    def get(self):
        students = models.User.query.filter_by(role=0)
        data = [marshal(student, student_fields) for student in students]
        return {'data': data}, HTTP_OK

    @auth_role(2, False)
    def post(self):
        student = models.User()
        student.id = request.json.get('id')
        student.password = request.json.get('password')
        student.name = request.json.get('username')
        student.role = 0
        if student.id is not None and student.password is not None:
            db.session.add(student)
            db.session.commit()
            return {}, HTTP_Created
        else:
            return {"message": "学生信息不全，补全后提交！"}, HTTP_Bad_Request

    @auth_role(0)
    def patch(self, student):
        name = request.json['username']
        password = request.json['password']
        student.name = student.name if name is None else name
        student.password = student.password if password is None else password
        try:
            db.session.commit()
        except Exception as e:
            return {"message": f"错误：{str(e)}"}, HTTP_Bad_Request
        return {}, HTTP_OK

# submit

submit_field = {
    'id': fields.Integer,
    'student_id': fields.String,
    'question_id': fields.Integer,
    'submit_sql': fields.String,
    'submit_time': fields.DateTime,
    'pass_rate': fields.Float,
    'status': fields.Integer
}

class Submits(Resource):
    # 获取自己的提交信息
    @auth_role(3)
    @marshal_with(submit_field)
    def get(self, submit_id, student):
        ret = models.Submission.query.filter_by(id=submit_id).first()
        
        if ret:
            if student and ret['student_id'] == student.id:
                return ret, HTTP_OK
            else:
                return {"message": "只可查看自己的提交信息。"}, HTTP_Forbidden
        else:
            return {"message": "该提交记录不存在"}, HTTP_NotFound

    # 删除提交信息
    @auth_role(2,False)
    def delete(self, submit_id):
        ret = models.Submission.query.filter_by(id=submit_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该提交记录不存在"}, HTTP_NotFound
    
    # 提交 - auth all
    @auth_role(3)
    def post(self):
        s = models.Submission()
        s.student_id = request.json['student_id']
        s.question_id = request.json['question_id']
        s.exam_id = request.json['request_id']
        s.submit_sql = request.json['submit_sql']
        s.submit_time = request.json['submit_time']
        s.pass_rate = 0
        s.status = -1

        if not (s.student_id and s.question_id and s.exam_id and s.submit_sql):
            return {"message": "提交信息不全"}, HTTP_Bad_Request
        
        db.session.add(s)
        db.session.commit()
        return {"message": "提交成功"}, HTTP_Created

class SubmitList(Resource):
    @auth_role(3)
    def get(self, admin, student, question_id=None, student_id=None):
        if question_id is None and student_id is None and student is not None:
            submits = models.Submission.query.filter_by(student_id=student.id)
        elif question_id is None and student_id is None and admin is not None:
            submits = models.Submission.query.filter_by()
        elif question_id is None and student is not None:
            submits = models.Submission.query.filter_by(student_id=student.id)
        elif question_id is not None and student_id is None:
            submits = models.Submission.query.filter_by(question_id=question_id)
        else:
            submits = models.Submission.query.filter_by(question_id=question_id, student_id=student_id)
        data = []
        for submit in submits:
            ret = marshal(submit, submit_field)
            data.append(ret)
        return {'data': data}, HTTP_OK
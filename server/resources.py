from flask import request
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
    'answer_example': fields.String
}

class Answers(Resource):
    @auth_role(AUTH_ALL)
    @marshal_with(answer_field)
    def get(self):
        question_id = request.json.get('question_id')
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            return ret, HTTP_OK
        else:
            return {"message": "该答案不存在"}, HTTP_NOT_FOUND

    @auth_role(AUTH_ADMIN)
    def delete(self):
        question_id = request.json.get('question_id')
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该答案不存在"}, HTTP_NOT_FOUND

# community
class Community(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        article_id = request.json.get("article_id")
        article = models.Article.query.filter_by(id=article_id)
        if article:
            return article, HTTP_OK
        else:
            return {"message": "文章不存在"}, HTTP_NOT_FOUND
    
    @auth_role(AUTH_ALL)
    def add(self):
        article = models.Article()
        article.title = request.json.get('title')
        article.user_id = request.json.get('user_id', None)
        article.question_id = request.json.get('user_id', None)
        article.is_notice = request.json.get('is_notice', False)
        article.content = request.json.get('content', None)
        article.publish_time = request.json.get('publish_time')
        article.last_modify_time = request.json.get('last_modify_time')
        if article.title and article.content:
            db.session.add(article)
            db.session.commit()
            return {}, HTTP_CREATED
        else:
            return {"message": "文章缺少标题或内容！"}, HTTP_BAD_REQUEST
    
    # TODO: 添加修改文章的类方法
    @auth_role(AUTH_ALL)
    def update(self):
        # 权限组
        role = request.json.get('role', AUTH_STUDENT)
        article_id = request.json.get('article_id')
        user_id = request.json.get('user_id')
        article = models.Article.query.filter_by(id=article_id)
        if not article:
            return {"message": "未找到文章！"}, HTTP_NOT_FOUND
        if role == AUTH_STUDENT and article.user_id != user_id:
            return {"message": "没有编辑权限！"}, HTTP_FORBIDDEN
        
        # 新文章内容
        newcontent = request.json.get('newcontent')
        if newcontent:
            article.content = newcontent
            db.session.add(article) # 更改文章，不确定add方法对不对
            db.session.commit()     # 提交更改
        
        return {}, HTTP_OK
            
    @auth_role(AUTH_ADMIN)
    def delete(self):
        article_id = request.json.get('article_id')
        article = models.Article.query.filter_by(id=article_id)
        if not article:
            return {"message": "未找到文章！"}, HTTP_NOT_FOUND
        
        # 删除文章
        db.session.remove(article)
        db.session.commit()
        return {}, HTTP_OK

# 文章列表类
community_field = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'user_id': fields.Integer,
    'question_id': fields.Integer,
    'publish_time': fields.DateTime,
    'is_notice': fields.Boolean
}
class CommunityList(Resource):
    @auth_role(AUTH_ALL)
    # @marshal_with(community_field)
    def get(self):
        articles = models.Article.query.all()
        data = [marshal(article, community_field) for article in articles]
        return {'data': data}, HTTP_OK
    


# TODO: Contest后端

# judge
# 定义返回结果的字段
submit_judge = {
    'submit_sql': fields.String,
    'question_id': fields.Integer
}

class SQLJudge(Resource):
    @auth_role(AUTH_ALL)
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
        engine = create_engine('mysql+pymysql://test:4546@localhost/testdb')
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

    def judge(self):
        """
        根据question_id从测试用例表读取对应的input_sql和output_sql，执行用户提交的SQL语句并判断结果
        :param submit_sql: 用户提交的SQL语句
        :param question_id: 问题ID
        :return: 测试结果字典，格式为 {测试用例ID: (error: bool, output: int)}
        """
        submit_sql = request.json.get('submit_sql')
        question_id = request.json.get('question_id')
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
                results[test_id] = (True, JUDGE_RUNERROR)  # 返回错误信息
                continue

            # 执行用户提交的SQL
            error, user_output = self.execute_sql(submit_sql)

            if error:  # 如果用户SQL执行出错
                if user_output == "TLE":  # 判断是否超时
                    results[test_id] = (True, JUDGE_TIMELIMIT_EXCEED)
                elif "MemoryError" in user_output:  # 判断是否内存溢出
                    results[test_id] = (True, JUDGE_MEMLIMIT_EXCEED)
                else:  # 其他错误
                    results[test_id] = (True, JUDGE_RUNERROR)
            elif user_output != expected_output:  # 判断输出是否正确
                results[test_id] = (True, JUDGE_WRONGANSWER)  # 输出错误
            else:
                results[test_id] = (False, JUDGE_ACCEPTED)  # 正确通过

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
            return {"message": '用户名或密码无效'}, HTTP_UNAUTHORIZED
        
    def logout(self):
        session = request.json.get('session')
        user = models.User.query.filter_by(session=session).first()
        if user:
            user.session = None
            db.session.commit()
            return {"message": '成功退出登录'}, HTTP_OK
        else:
            return {"message": '身份信息无效！请重新登录。'}, HTTP_UNAUTHORIZED
        
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
            return {"message": '身份信息无效！请重新登录。'}, HTTP_UNAUTHORIZED

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
    @auth_role(AUTH_ALL)
    @marshal_with(question_field)
    def get(self):
        # 查询单个题目 -> 用于题目查询和显示
        question_id = request.json.get('question_id')
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            return ret, HTTP_OK
        else:
            return {"message": "该题目不存在"}, HTTP_NOT_FOUND

    @auth_role(AUTH_ADMIN)
    def delete(self):
        question_id = request.json.get('question_id')
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该题目不存在"}, HTTP_NOT_FOUND
    
    @auth_role(AUTH_ADMIN)
    def post(self):
        q = models.Question()
        q.title = request.json['title']
        q.description = request.json['description']
        q.difficulty = request.json['difficulty']
        q.answer_example = request.json['answer_example']
        if not (q.title and q.description and q.difficulty and q.answer_example):
            return {"message": "题目信息不全，补全缺失项！"}, HTTP_BAD_REQUEST
        db.session.add(q)
        db.session.commit()
        return {"message": "新增题目成功"}, HTTP_CREATED

# 处理题目列表的相关功能
class QuestionList(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        # 查询所有题目 -> 用于题目列表的查询和显示
        questions = models.Question.query.all()
        data = [marshal(question, question_field) for question in questions]
        
        return {'data': data}, HTTP_OK

# register
class Register(Resource):
    def post(self):
        id = request.json.get('id', None)
        username = request.json.get('username', None)
        password = hashlib.sha256(request.json.get('password', 0).encode('utf8')).hexdigest() 
        
        if models.User.query.filter_by(id=id).first():
            return {"message": "ID撞车了，换一个。"}, HTTP_CONFLICT
        if models.User.query.filter_by(username=username).first():
            return {"message": "有人跟你重名了，换一个。"}, HTTP_CONFLICT
        
        new_user = models.User(id=id, username=username, password=password, role=AUTH_STUDENT)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "成了，快去登录吧！"}, HTTP_CREATED

# students
student_fields = {
    'id': fields.Integer,
    'username': fields.String
}

class Students(Resource):
    @auth_role(AUTH_ALL)
    @marshal_with(student_fields)
    def get(self):
        student_id = request.json.get('student_id')
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            return ret, HTTP_OK
        else:
            return {"message": "该学生不存在"}, HTTP_NOT_FOUND
        
    @auth_role(AUTH_ADMIN)
    def delete(self):
        student_id = request.json.get('student_id')
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该学生不存在"}, HTTP_NOT_FOUND

    @auth_role(AUTH_ADMIN)
    def add(self):
        student = models.User()
        student.id = request.json.get('id')
        student.password = request.json.get('password')
        student.username = request.json.get('username')
        student.role = AUTH_STUDENT
        if student.id and student.password:
            ret = models.User.query.filter_by(id=student.id).first()
            if ret:
                return {"message": "该学生已存在"}, HTTP_CONFLICT
            db.session.add(student)
            db.session.commit()
            return {}, HTTP_CREATED
        else:
            return {"message": "学生信息不全，补全后提交！"}, HTTP_BAD_REQUEST
    
    # TODO: 添加修改学生信息的函数

class StudentList(Resource):
    @auth_role(AUTH_ADMIN)
    def get(self):
        students = models.User.query.filter_by(role=AUTH_STUDENT)
        data = [marshal(student, student_fields) for student in students]
        return {'data': data}, HTTP_OK

# submit
submit_field = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'question_id': fields.Integer,
    "exam_id": fields.Integer,
    'submit_sql': fields.String,
    'submit_time': fields.DateTime,
    'pass_rate': fields.Float
}

class Submits(Resource):
    # 获取自己的提交信息
    @auth_role(AUTH_ALL)
    @marshal_with(submit_field)
    def get(self):
        submit_id = request.json.get('submit_id')
        student = request.json.get('student')
        ret = models.Submission.query.filter_by(id=submit_id).first()
        if ret:
            if student and ret['student_id'] == student.id:
                return ret, HTTP_OK
            else:
                return {"message": "只可查看自己的提交信息。"}, HTTP_FORBIDDEN
        else:
            return {"message": "该提交记录不存在"}, HTTP_NOT_FOUND

    # 删除提交信息
    @auth_role(AUTH_ADMIN)
    def delete(self):
        submit_id = request.json.get("submit_id")
        ret = models.Submission.query.filter_by(id=submit_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该提交记录不存在"}, HTTP_NOT_FOUND
    
    # 提交 - auth all
    @auth_role(AUTH_ALL)
    def post(self):
        s = models.Submission()
        s.student_id = request.json['student_id']
        s.question_id = request.json['question_id']
        s.exam_id = request.json['request_id']
        s.submit_sql = request.json['submit_sql']
        s.submit_time = request.json['submit_time']
        s.pass_rate = 0
        s.status = JUDGE_PENDING

        if not (s.student_id and s.question_id and s.exam_id and s.submit_sql):
            return {"message": "提交信息不全"}, HTTP_BAD_REQUEST
        
        db.session.add(s)
        db.session.commit()
        return {"message": "提交成功"}, HTTP_CREATED

class SubmitList(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        role = request.json.get('role', AUTH_STUDENT)
        student_id = request.json.get('student_id', None)
        if role > AUTH_STUDENT:
            submits = models.Submission.query.filter_by()
        elif student_id:
            submits = models.Submission.query.filter_by(student_id=student_id)
        else:
            return {"message": "学生不存在！"}, HTTP_BAD_REQUEST
        data = [marshal(submit, submit_field) for submit in submits]
        return {'data': data}, HTTP_OK
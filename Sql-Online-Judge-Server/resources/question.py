from flask_restful import Resource, fields, marshal_with, marshal
import models
from exts import db
from common.comm import auth_role, auth_all
from config import *
from flask import request

# ws3917 - 题目基本信息
question_field = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'difficulty': fields.Integer,
    'answer_example': fields.String
}

# 处理单个题目的相关功能
class Questions(Resource):

    @auth_all(False)
    @marshal_with(question_field)
    def get(self, question_id):
        # 查询单个题目 -> 用于题目查询和显示
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            return ret, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_role(2, False)
    def delete(self, question_id):
        # 删除单个题目 -> 可能管理员用得到，但一般用户用不到
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_role(2, False)
    def patch(self, question_id):
        # 更新单个题目的信息 -> 可能管理员用得到，但一般用户用不到
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            title = request.json.get('title')
            description = request.json.get('description')
            difficulty = request.json.get('difficulty')
            answer_example = request.json.get('answer_example')
            ret.title = ret.title if title is None else title
            ret.description = ret.description if description is None else description
            ret.difficulty = ret.difficulty if difficulty is None else difficulty
            ret.answer_example = ret.answer_example if answer_example is None else answer_example
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound
    
    @auth_role(2, False)
    def post(self):
        # 创建新的题目 -> 可能管理员用得到，但一般用户用不到
        q = models.Question()
        q.title = request.json['title']
        q.description = request.json['description']
        q.difficulty = request.json['difficulty']
        q.answer_example = request.json['answer_example']
        if q.title is None or q.description is None or q.difficulty is None or q.answer_example is None:
            return {"message": "题目信息不全，补全缺失项！"}, HTTP_Bad_Request
        db.session.add(q)
        db.session.commit()
        return {}, HTTP_Created

# 处理题目列表的相关功能
class QuestionList(Resource):
    @auth_all(inject=True)
    def get(self, student, admin):
        # 查询所有题目 -> 用于题目列表的查询和显示
        questions = models.Question.query.filter_by()
        data = [marshal(q, question_field) for q in questions]
        return {'data': data}, HTTP_OK


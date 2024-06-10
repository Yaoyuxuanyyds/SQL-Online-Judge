from flask_restful import Resource, fields, marshal_with, marshal
import models
from exts import db
from common.comm import auth_admin, auth_all
from config import *
from flask import request

question_field = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'difficulty': fields.Integer,
    'standard_answer': fields.String
}

class Questions(Resource):

    @auth_all(False)
    @marshal_with(question_field)
    def get(self, question_id):
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret is not None:
            return ret, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_admin(False)
    def delete(self, question_id):
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret is not None:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_admin(False)
    def patch(self, question_id):
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret is not None:
            title = request.json.get('title')
            description = request.json.get('description')
            difficulty = request.json.get('difficulty')
            standard_answer = request.json.get('standard_answer')
            ret.title = ret.title if title is None else title
            ret.description = ret.description if description is None else description
            ret.difficulty = ret.difficulty if difficulty is None else difficulty
            ret.standard_answer = ret.standard_answer if standard_answer is None else standard_answer
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

class QuestionList(Resource):

    @auth_all(inject=True)
    def get(self, student, admin):
        questions = models.Question.query.filter_by()
        data = [marshal(q, question_field) for q in questions]
        return {'data': data}, HTTP_OK

    @auth_admin(inject=False)
    def post(self):
        q = models.Question()
        q.title = request.json['title']
        q.description = request.json['description']
        q.difficulty = request.json['difficulty']
        q.standard_answer = request.json['standard_answer']
        if q.title is None or q.description is None or q.difficulty is None or q.standard_answer is None:
            return get_shortage_error_dic("title description difficulty standard_answer"), HTTP_Bad_Request
        db.session.add(q)
        db.session.commit()
        return {}, HTTP_Created

from flask_restful import Resource, fields, marshal_with, marshal
import models
from exts import db
from common.comm import auth_role, auth_all
from config import *
from flask import request

answer_field = {
    'id': fields.Integer,
    'idQuestion': fields.Integer,
    'sql': fields.String,
    'json': fields.String,
}

class Answers(Resource):

    @auth_all(False)
    @marshal_with(answer_field)
    def get(self, idQuestion, answer_id):
        ret = models.Answer.query.filter_by(id=answer_id).first()
        if ret is not None:
            return ret, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_role(2, False)
    def delete(self, idQuestion, answer_id):
        ret = models.Answer.query.filter_by(id=answer_id).first()
        if ret is not None:
            question = ret.Question
            db.session.delete(ret)
            db.session.commit()
            answer_left = models.Answer.query.filter_by(idQuestion=question.id).first()
            if answer_left is None:
                question.result = None
                db.session.commit()
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_role(2,False)
    def patch(self, answer_id):
        ret = models.Answer.query.filter_by(id=answer_id).first()
        if ret is not None:
            pass
        else:
            return {}, HTTP_NotFound

class AnswerList(Resource):

    @auth_all(inject=False)
    def get(self, idQuestion):
        answers = models.Answer.query.filter_by(idQuestion=idQuestion)
        data = [marshal(answer, answer_field) for answer in answers]
        return {'data': data}, HTTP_OK

    @auth_role(2,inject=False)
    def post(self, idQuestion):
        answer = models.Answer()
        answer.idQuestion = idQuestion
        question = models.Question.query.get(answer.idQuestion)
        answer.sql = request.json.get('sql')
        if answer.idQuestion is None or answer.sql is None:
            return get_shortage_error_dic("idQuestion data"), HTTP_Bad_Request
        if question is None:
            return get_common_error_dic("question id is wrong"), HTTP_Bad_Request

        db.session.add(answer)
        db.session.commit()

        return {}, HTTP_Created

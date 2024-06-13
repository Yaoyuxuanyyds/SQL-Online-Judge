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
        if ret:
            return ret, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_role(2, False)
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
            return {}, HTTP_NotFound

    @auth_role(2,False)
    def patch(self, answer_id):
        ret = models.Answer.query.filter_by(id=answer_id).first()
        if ret:
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

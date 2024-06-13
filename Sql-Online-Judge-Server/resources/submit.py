from flask_restful import Resource, fields, marshal_with, marshal, reqparse
import models
from exts import db
from common.comm import auth_role, auth_all
from config import *
from flask import request
import json
from config import type_submit

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

    @auth_all()
    @marshal_with(submit_field)
    def get(self, admin, student, submit_id, student_id):
        if student is not None and student.id != student_id:
            return get_common_error_dic("you not allow to access this resource"), HTTP_Forbidden
        ret = models.Submission.query.filter_by(id=submit_id).first()
        if ret:
            return ret, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_role(2,False)
    def delete(self, submit_id, student_id):
        ret = models.Submission.query.filter_by(id=submit_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

class SubmitList(Resource):

    @auth_all(inject=True)
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

    @auth_role(0)
    def post(self, question_id, student, student_id=None):
        if student_id is not None and student_id != student.id:
            return get_common_error_dic('student id not match your account!'), HTTP_Forbidden
        submit = models.Submission()
        submit.student_id = student.id
        submit.question_id = question_id
        submit.submit_sql = request.json.get('submit_sql')
        submit.pass_rate = 1.0
        submit.status = 0
        if submit.question_id is None or submit.submit_sql is None:
            return get_shortage_error_dic('question_id or submit_sql'), HTTP_Bad_Request
        db.session.add(submit)
        db.session.commit()
        return {
            'id': submit.id,
            'status': submit.status,
            'submit_sql': submit.submit_sql,
            'submit_time': submit.submit_time.isoformat(),
            'pass_rate': submit.pass_rate
        }, HTTP_Created

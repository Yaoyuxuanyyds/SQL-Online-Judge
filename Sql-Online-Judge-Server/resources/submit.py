from flask_restful import Resource, fields, marshal_with, marshal, reqparse
import models, time
from exts import db
from resources.permissions import auth_role
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
        s.exam_id = request.json['request_id']
        s.submit_sql = request.json['submit_sql']
        s.submit_time = request.json['submit_time']
        s.pass_rate = 0
        s.status = 0

        if not (s.student_id and s.exam_id and s.submit_sql):
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
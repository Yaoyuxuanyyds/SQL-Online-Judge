from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal
import models
from exts import db
from common.comm import auth_role
from config import *
from flask import request

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
            return {}, HTTP_NotFound

    def delete(self, student_id):
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

    def put(self, student_id):
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            ret.password = request.json['password']
            ret.name = request.json['username']
            try:
                db.session.commit()
            except Exception as e:
                return get_except_error(e)
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

    def patch(self, student_id):
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            ret.password = ret.password if request.json['password'] is None else request.json['password']
            ret.name = ret.name if request.json['username'] is None else request.json['username']
            try:
                db.session.commit()
            except Exception as e:
                return get_except_error(e)
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

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
            return get_shortage_error_dic('id password username'), HTTP_Bad_Request

    @auth_role(0)
    def patch(self, student):
        name = request.json['username']
        password = request.json['password']
        student.name = student.name if name is None else name
        student.password = student.password if password is None else password
        try:
            db.session.commit()
        except Exception as e:
            return get_except_error(e)
        return {}, HTTP_OK

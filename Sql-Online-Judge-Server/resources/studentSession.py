import hashlib
import os

from flask_restful import Resource, reqparse, abort
from models import User
from exts import db
from common.comm import auth_role

student_login_parser = reqparse.RequestParser()
student_login_parser.add_argument('id', location='json', required=True, help='ID不能为空')
student_login_parser.add_argument('password', location='json', required=True, help='密码不能为空')

class StudentSession(Resource):

    @auth_role(0)
    def get(self, student):
        return {'name': student.username, 'id': student.id}, 200

    @auth_role(0)
    def delete(self, student):
        student.session = None
        db.session.commit()
        return {}, 200

import hashlib
import os

from flask_restful import Resource, reqparse, abort
from models import User
from exts import db
from resources.permissions import auth_teacher

teacher_login_parser = reqparse.RequestParser()
teacher_login_parser.add_argument('id', location='json', required=True, help='ID不能为空')
teacher_login_parser.add_argument('password', location='json', required=True, help='密码不能为空')

class TeacherSession(Resource):

    @auth_teacher
    def get(self, teacher):
        return {'name': teacher.username, 'id': teacher.id}, 200
    
    @auth_teacher
    def delete(self, teacher):
        teacher.session = None
        db.session.commit()
        return {}, 200

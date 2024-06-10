import hashlib
import os

from flask_restful import Resource, reqparse, abort
from models import User
from exts import db
from common.comm import auth_student

student_login_parser = reqparse.RequestParser()
student_login_parser.add_argument('id', location='json', required=True, help='ID不能为空')
student_login_parser.add_argument('password', location='json', required=True, help='密码不能为空')

class StudentSession(Resource):

    @auth_student
    def get(self, student):
        return {'name': student.username, 'id': student.id}, 200

    def post(self):
        args = student_login_parser.parse_args()
        id = args["id"]
        password = args["password"]
        ret = User.query.filter_by(id=id, password=password, role=0).first()  # role 0 for student
        if ret is not None:
            student_session = hashlib.sha1(os.urandom(24)).hexdigest()
            ret.session = student_session
            db.session.commit()
            return {"session": student_session, 'name': ret.username}, 201
        abort(401)

    @auth_student
    def delete(self, student):
        student.session = None
        db.session.commit()
        return {}, 200

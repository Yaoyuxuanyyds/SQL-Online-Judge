import hashlib
import os

from flask_restful import Resource, reqparse, abort
from models import User
from exts import db
from common.comm import auth_teacher

teacher_login_parser = reqparse.RequestParser()
teacher_login_parser.add_argument('id', location='json', required=True, help='ID不能为空')
teacher_login_parser.add_argument('password', location='json', required=True, help='密码不能为空')

class TeacherSession(Resource):

    @auth_teacher
    def get(self, teacher):
        return {'name': teacher.username, 'id': teacher.id}, 200

    def post(self):
        args = teacher_login_parser.parse_args()
        id = args["id"]
        password = args["password"]
        ret = User.query.filter_by(id=id, password=password, role=1).first()  # role 1 for teacher
        if ret is not None:
            teacher_session = hashlib.sha1(os.urandom(24)).hexdigest()
            ret.session = teacher_session
            db.session.commit()
            return {"session": teacher_session, 'name': ret.username}, 201
        abort(401)

    @auth_teacher
    def delete(self, teacher):
        teacher.session = None
        db.session.commit()
        return {}, 200

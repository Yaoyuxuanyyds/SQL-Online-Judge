import hashlib
import os

from flask_restful import Resource, reqparse, abort
from models import User
from exts import db
from common.comm import auth_admin

admin_login_parser = reqparse.RequestParser()
admin_login_parser.add_argument('id', location='json')
admin_login_parser.add_argument('password', location='json')

class AdminSession(Resource):

    @auth_admin
    def get(self, admin):
        return {'name': admin.username}, 200

    def post(self):
        args = admin_login_parser.parse_args()
        ret = User.query.filter_by(id=args["id"], password=args["password"], role=2).first()  # role 2 for admin
        if ret is not None:
            admin_session = hashlib.sha1(os.urandom(24)).hexdigest()
            ret.session = admin_session
            db.session.commit()
            return {"session": admin_session, "name": ret.username}, 201
        abort(401)

    @auth_admin
    def delete(self, admin):
        admin.session = None
        db.session.commit()
        return {}, 200

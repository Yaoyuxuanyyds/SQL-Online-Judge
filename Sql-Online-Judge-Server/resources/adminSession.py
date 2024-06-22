import hashlib
import os
from flask_restful import Resource, reqparse, abort
from models import User
from exts import db
from common.comm import auth_role

admin_login_parser = reqparse.RequestParser()
admin_login_parser.add_argument('id', location='json')
admin_login_parser.add_argument('password', location='json')

class AdminSession(Resource):

    @auth_role(2)
    def get(self, admin):
        return {'name': admin.username}, 200

    @auth_role(2)
    def delete(self, admin):
        admin.session = None
        db.session.commit()
        return {}, 200

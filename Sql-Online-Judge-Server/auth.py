from flask import Blueprint, request, jsonify, abort
from models import User
from exts import db
import hashlib
import os

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('id')
    password = data.get('password')
    user = User.query.filter_by(id=user_id, password=password).first()

    if user:
        session_token = hashlib.sha1(os.urandom(24)).hexdigest()
        user.session = session_token
        db.session.commit()
        return jsonify(session=session_token, role=user.role, name=user.username), 200
    else:
        return jsonify(message='用户名或密码无效'), HTTP_Unauthorized

@auth.route('/api/logout', methods=['POST'])
def logout():
    session = request.json.get('session')
    user = User.query.filter_by(session=session).first()
    if user:
        user.session = None
        db.session.commit()
        return jsonify(message='成功退出登录'), 200
    else:
        return jsonify(message='身份信息无效！'), HTTP_Unauthorized

@auth.route('/api/session', methods=['GET'])
def get_session():
    session = request.headers.get('session')
    user = User.query.filter_by(session=session).first()
    if user:
        return jsonify(id=user.id, name=user.username, role=user.role), 200
    else:
        return jsonify(message='身份信息无效！'), HTTP_Unauthorized

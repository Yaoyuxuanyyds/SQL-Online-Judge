from flask import request
from functools import wraps
from models import User
from flask_restful import abort

def get_session():
    if request.method == 'GET':
        return request.headers.get('session')
    elif request.json is not None:
        return request.json.get('session')
    return None

def auth_admin(inject=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = get_session()
            if session is None:
                abort(400)
            ret = User.query.filter_by(session=session, role=2).first()  # role 2 for admin
            if ret is None:
                abort(401)
            if inject:
                return func(admin=ret, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def auth_student(inject=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = get_session()
            if session is None:
                abort(400)
            ret = User.query.filter_by(session=session, role=0).first()  # role 0 for student
            if ret is None:
                abort(401)
            if inject:
                return func(student=ret, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def auth_teacher(inject=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = get_session()
            if session is None:
                abort(400)
            ret = User.query.filter_by(session=session, role=1).first()  # role 1 for teacher
            if ret is None:
                abort(401)
            if inject:
                return func(teacher=ret, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def auth_all(inject=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = get_session()
            if session is None:
                abort(400)
            ret_student = User.query.filter_by(session=session, role=0).first()
            ret_teacher = User.query.filter_by(session=session, role=1).first()
            ret_admin = User.query.filter_by(session=session, role=2).first()
            if ret_admin is None and ret_student is None and ret_teacher is None:
                abort(401)
            if inject:
                return func(student=ret_student, teacher=ret_teacher, admin=ret_admin, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

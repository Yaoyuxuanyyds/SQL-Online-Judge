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

def auth_role(role, inject=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = get_session()
            if session is None:
                abort(400)
            user = User.query.filter_by(session=session, role=role).first()
            if user is None:
                abort(401)
            if inject:
                return func(user=user, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

auth_admin = auth_role(2)
auth_teacher = auth_role(1)
auth_student = auth_role(0)

def auth_all(inject=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = get_session()
            if session is None:
                abort(400)
            user = User.query.filter_by(session=session).first()
            if user is None:
                abort(401)
            if inject:
                return func(user=user, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

from flask import request
from functools import wraps
from flask_restful import abort
import models
from config import *
# permissions
def get_session():
    if request.method == 'GET':
        return request.headers.get('session')
    
    # 检查是否为 JSON 请求并处理异常
    if request.is_json:
        return request.json.get('session', None)
    
    # 检查是否为表单数据请求
    if request.form:
        return request.form.get('session', None)
    
    # 检查是否为其他类型的请求数据，例如 URL 参数
    if request.args:
        return request.args.get('session', None)
    
    return None

def auth_role(role, inject=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = get_session()
            if session is None:
                abort(HTTP_Bad_Request)
            if role == 3:       # role = 3 即为all
                user = models.User.query.filter_by(session=session).first()
            else:
                # role = 0 学生，1 老师，2 管理员
                user = models.User.query.filter_by(session=session, role=role).first()
            if user is None:
                abort(HTTP_Unauthorized)
            if inject:
                return func(user=user, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

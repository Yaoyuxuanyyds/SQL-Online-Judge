from flask_restful import Resource, reqparse, abort
from models import User
from exts import db

register_parser = reqparse.RequestParser()
register_parser.add_argument('id', type=int, required=True, help='ID不能为空')
register_parser.add_argument('username', type=str, required=True, help='用户名不能为空')
register_parser.add_argument('password', type=str, required=True, help='密码不能为空')

class Register(Resource):
    def post(self):
        args = register_parser.parse_args()
        id = args['id']
        username = args['username']
        password = args['password']
        
        if User.query.filter_by(id=id).first():
            return {"message": "ID已存在"}, 409
        if User.query.filter_by(username=username).first():
            return {"message": "用户名已存在"}, 409
        
        new_user = User(id=id, username=username, password=password, role=0)  # 默认角色为0
        db.session.add(new_user)
        db.session.commit()
        return {"message": "注册成功"}, 201

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
        print(args)
        id = args.get('id', "")
        username = args.get('username', "")
        password = args.get('password', "")

        if not id:
            return {"message": "没ID没成绩！"}, 403
        if not username:
            return {"message": "不给名字谁认识你叫啥？"}, 403
        if not password:
            return {"message": "你不怕号被盗？"}, 403

        if User.query.filter_by(id=id).first():
            return {"message": "ID撞车了，换一个。"}, 409
        if User.query.filter_by(username=username).first():
            return {"message": "有人跟你重名了，换一个。"}, 409
        
        new_user = User(id=id, username=username, password=password, role=0)  # 默认角色为0
        db.session.add(new_user)
        db.session.commit()
        return {"message": "成了，快去登录吧！"}, 201

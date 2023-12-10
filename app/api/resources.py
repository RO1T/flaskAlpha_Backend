from flask_restful import Resource, reqparse, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, users

registerParser = reqparse.RequestParser()
registerParser.add_argument("login", type=str)
registerParser.add_argument("password", type=str)
registerParser.add_argument("email", type=str)
registerParser.add_argument("role", type=str)

loginParser = reqparse.RequestParser()
loginParser.add_argument("login", type=str)
loginParser.add_argument("password", type=str)

class Register(Resource):
    def post(self):
        try:
            user = registerParser.parse_args()
            user["password"] = generate_password_hash(user["password"])
            new_user = users(login=user["login"], password=user["password"],
                             email=user["email"], role=user["role"])
            db.session.add(new_user)
            db.session.commit()
            return {"message": "user created"}, 201
        except Exception as e:
            abort(500, "user registering error")

class GetUsers(Resource):
    def get(self):
        try:
            users_lst = users.query.all()
            users_slv = {}
            for user in users_lst:
                users_slv[user.id] = {"login": user.login, "password": user.password,
                                      "email": user.email, "role": user.role}
            return users_slv, 200
        except Exception as e:
            abort(500, message="users getting error")

class Login(Resource):
    def post(self):
        try:
            user = loginParser.parse_args()
            user_in_base = users.query.filter_by(login=user["login"]).first()
            if user_in_base:
                if (check_password_hash(user_in_base.password, user["password"])):
                    return {"message": "successful authorization"}, 200
                else:
                    return {"message": "password is not correct"}, 400
            return {"message": "user is not found"}, 404
        except Exception as e:
            abort(500, message="user getting error")
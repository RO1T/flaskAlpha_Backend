from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, get_current_user
from app.models import db, users, tokenblocklist, surveys

registerParser = reqparse.RequestParser()
registerParser.add_argument("login", type=str)
registerParser.add_argument("password", type=str)
registerParser.add_argument("email", type=str)
registerParser.add_argument("role", type=str)

loginParser = reqparse.RequestParser()
loginParser.add_argument("login", type=str)
loginParser.add_argument("password", type=str)

surveyCreateParser = reqparse.RequestParser()
surveyCreateParser.add_argument("title", type=str)
surveyCreateParser.add_argument("description", type=str)
surveyCreateParser.add_argument("logoPosition", type=str)
surveyCreateParser.add_argument("date_creation", type=str)
surveyCreateParser.add_argument("pages", type=list)

class Register(Resource):
    def post(self):
        user = registerParser.parse_args()
        user["password"] = generate_password_hash(user["password"])
        new_user = users(login=user["login"], hash_password=user["password"],
                            email=user["email"], role=user["role"])
        if users.query.filter_by(email=user["login"]).first():
            return {'message': 'User {} already exists'.format(user['login'])}
        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': "user was created"}, 201
        except Exception as e:
            return {"message": "Something went wrong"}, 500

class GetUsers(Resource):
    def get(self):
        try:
            users_lst = users.query.all()
            users_slv = {}
            for user in users_lst:
                users_slv[user.id] = {"login": user.login, "password": user.hash_password,
                                      "email": user.email, "role": user.role}
            return users_slv, 200
        except Exception as e:
            {"message": "Something went wrong"}, 500

class Login(Resource):
    def post(self):
        try:
            user = loginParser.parse_args()
            user_in_base = users.query.filter_by(login=user["login"]).first()
            if user_in_base:
                if (check_password_hash(user_in_base.hash_password, user["password"])):
                    access_token = create_access_token(identity=user['login'])
                    refresh_token = create_refresh_token(identity=user['login'])
                    return {"message": "successful authorization",
                            'access_token': access_token,
                            'refresh_token': refresh_token
                            }, 200
                else:
                    return {"message": "password is not correct"}, 400
            return {"message": "user is not found"}, 404
        except Exception as e:
            {"message": "Something went wrong"}, 500

class Logout(Resource):
    @jwt_required()
    def delete(self):
        jti = get_jwt()["jti"]
        db.session.add(tokenblocklist(jti=jti))
        db.session.commit()
        return {"msg": "JWT revoked"}, 200

class Secret(Resource):
    @jwt_required()
    def get(self):
        return {'answer': 42}
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}, 200

class CreateSurvey(Resource):
    @jwt_required()
    def post(self):
        survey = surveyCreateParser.parse_args()
        user = users.query.filter_by(login=get_current_user()).first()
        new_survey = surveys(title=survey["title"], description=survey["description"],
                             logoPosition=survey["logoPosition"], date_creation=survey["date_creation"],
                             pages=survey["pages"], user_id=user.id)
        db.session.add(new_survey)
        db.session.commit()
        return {"msg": "success"}


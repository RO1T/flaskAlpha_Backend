from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, \
    get_current_user
from app.models import db, users, tokenblocklist, surveys, pages, questions, answers, profiles
from app.parsers.parsers import registerParser, loginParser, profileParser, surveyCreateParser, answerSendParser

class Register(Resource):
    def post(self):
        try:
            user = registerParser.parse_args()
            user_in_base = users.query.filter_by(login=user["login"]).first()
            if user_in_base:
                return {'msg': 'User {} already exists'.format(user['login'])}
            else:
                user["password"] = generate_password_hash(user["password"])
                new_user = users(login=user["login"], hash_password=user["password"],
                                    email=user["email"], role=user["role"])
                db.session.add(new_user)
                db.session.commit()
                return {'msg': "user was created"}, 201
        except Exception as e:
            return {"msg": "Something went wrong"}, 500

class GetUsers(Resource):
    @jwt_required()
    def get(self, user_id=None):
        try:
            if user_id == None:
                users_lst = users.query.all()
            else:
                users_lst = users.query.filter_by(id=user_id).all()
            if users_lst:
                users_slv = {}
                for user in users_lst:
                    users_slv[user.id] = {"login": user.login, "password": user.hash_password,
                                            "email": user.email, "role": user.role}
                return users_slv, 200
            else:
                return {"msg": "user is not found"}
        except Exception as e:
            {"msg": "Something went wrong"}, 500

class Login(Resource):
    def post(self):
        try:
            user = loginParser.parse_args()
            user_in_base = users.query.filter_by(login=user["login"]).first()
            if user_in_base:
                if (check_password_hash(user_in_base.hash_password, user["password"])):
                    access_token = create_access_token(identity=user['login'])
                    refresh_token = create_refresh_token(identity=user['login'])
                    return {"msg": "successful authorization",
                            'access_token': access_token
                            }, 200
                else:
                    return {"msg": "password is not correct"}, 400
            return {"msg": "user is not found"}, 404
        except Exception as e:
            {"msg": "login error"}, 500

class Profile(Resource):
    @jwt_required()
    def post(self):
        try:
            profile = profileParser.parse_args()
            user = users.query.filter_by(login=get_current_user()).first()
            profile_in_base = profiles.query.filter_by(user_id=user.id).first()
            username_in_base = profiles.query.filter_by(username=profile.username).first()
            if profile_in_base or username_in_base:
                return {"msg": "this user or username already exists"}, 201
            else:
                new_profile = profiles(username=profile["username"], avatar_url=profile.get("avatar_url"),
                                       user_id=user.id)
                db.session.add(new_profile)
                db.session.commit()
                return {"msg": "success"}, 200
        except Exception as e:
            return {"msg": "create profile error"}, 500

    @jwt_required()
    def put(self):
        try:
            profile_args = profileParser.parse_args()
            user = users.query.filter_by(login=get_current_user()).first()
            profile = profiles.query.filter_by(user_id=user.id).first()
            username_in_base = profiles.query.filter_by(username=profile_args.username).first()
            if not username_in_base:
                profile.username = profile_args["username"]
                db.session.commit()
                return {"msg": "success change username"}, 200
            else:
                return {"msg": "this username already exists"}, 400
        except Exception as e:
            return {"msg": "refresh profile info error"}, 500

    @jwt_required()
    def get(self):
        try:
            user = users.query.filter_by(login=get_current_user()).first()
            profile = profiles.query.filter_by(user_id=user.id).first()
            if profile:
                profile_slv = {"username": profile.username, "avatar_url": profile.avatar_url, "balance": profile.balance,
                            "completed_surveys": profile.complete_survey}
                return profile_slv, 200
            else:
                return {"msg": "not profile"}, 201
        except Exception as e:
            return {"msg": "get profile error"}, 500

class Logout(Resource):
    @jwt_required()
    def delete(self):
        try:
            jti = get_jwt()["jti"]
            db.session.add(tokenblocklist(jti=jti))
            db.session.commit()
            return {"msg": "logout success"}, 200
        except Exception as e:
            return {"msg": "logout error"}, 500

class CreateSurvey(Resource):
    @jwt_required()
    def post(self):
        try:
            user = users.query.filter_by(login=get_current_user()).first()
            if user.role == "b":
                survey = surveyCreateParser.parse_args()
                new_survey = surveys(title=survey["title"], description=survey["description"],
                                     logoPosition=survey["logoPosition"], value=survey["value"],
                                     pages=[], user_id=user.id)
                db.session.add(new_survey)
                db.session.flush()
                for i in range(len(survey["pages"])):
                    new_page = pages(name=survey["pages"][i]["page_name"], elements=[],
                                     surveys_id=new_survey.id)
                    db.session.add(new_page)
                    db.session.flush()
                    for j in range(len(survey["pages"][i]["elements"])):
                        new_question = questions(type=survey["pages"][i]["elements"][j]["type"],
                                                 name=survey["pages"][i]["elements"][j]["name"],
                                                 isRequired=survey["pages"][i]["elements"][j].get("isRequired"),
                                                 title=survey["pages"][i]["elements"][j].get("title"),
                                                 placeholder=survey["pages"][i]["elements"][j].get("placeholder"),
                                                 choices=survey["pages"][i]["elements"][j].get("choices"),
                                                 page_id=new_page.id,)
                        db.session.add(new_question)
                db.session.commit()
                return {"msg": "success"}, 201
            else:
                return {"msg": "you dont have permission"}
        except Exception as e:
            return {"msg": f"survey create error {e}"}, 500

class SendAnswers(Resource):
    @jwt_required()
    def post(self, survey_id):
        try:
            user = users.query.filter_by(login=get_current_user()).first()
            answer = answerSendParser.parse_args()
            survey = surveys.query.filter_by(id=survey_id).first()
            page_lst = pages.query.filter_by(surveys_id=survey_id).all()
            for page in page_lst:
                question_lst = questions.query.filter_by(page_id=page.id).all()
                for i in range(len(question_lst)):
                    new_answer = answers(title=question_lst[i].name, answer=answer["answers"][i],
                                         question_id=question_lst[i].id, user_id=user.id)
                    db.session.add(new_answer)
            profile = profiles.query.filter_by(user_id=user.id).first()
            profile.balance += survey.value
            profile.complete_survey += 1
            db.session.commit()
            return {"msg": "answers has been add"}, 200
        except Exception as e:
            return {"msg": "answers add error"}, 500

class GetSurveys(Resource):
    @jwt_required()
    def get(self, survey_id=None):
        try:
            if survey_id is None:
                surveys_lst = surveys.query.all()
            else:
                surveys_lst = surveys.query.filter_by(id=survey_id).all()
            if surveys_lst:
                surveys_dict = {}
                for survey in surveys_lst:
                    surveys_dict[survey.id] = {"title": survey.title, "description": survey.description,
                                                "logoPosition": survey.logoPosition,
                                                "date_creation": survey.date_creation.strftime("%Y-%m-%d %H:%M:%S"),
                                                "value": survey.value,
                                                "pages": [], "user_id": survey.user_id}
                return surveys_dict, 200
            else:
                return {"msg": "survey is not found"}
        except Exception as e:
            return {"msg": f"getting surveys error {e}"}, 500

class CompleteSurvey(Resource):
    @jwt_required()
    def get(self, survey_id):
        try:
            if survey_id:
                survey_slv = {}
                survey = surveys.query.filter_by(id=survey_id).first()
                page = pages.query.filter_by(surveys_id=survey_id).all()
                for p in page:
                    element = questions.query.filter_by(page_id=p.id).all()
                    for e in element:
                        p.elements.append(e.serialize())
                    pg_name = {"name": p.name, "elements": p.elements}
                    survey.pages.append(pg_name)
                survey_slv[survey_id] = {"title": survey.title, "description": survey.description,
                                         "logoPosition": survey.logoPosition,
                                         "date_creation": survey.date_creation.strftime("%Y-%m-%d %H:%M:%S"),
                                         "value": survey.value, "pages": survey.pages}
                return survey_slv, 200
            else:
                return {"msg": "necessary id"}, 400
        except Exception as e:
            return {"msg": f"get survey for complete error {e}"}, 500
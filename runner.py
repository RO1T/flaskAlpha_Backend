from flask import Flask, render_template
from flask_restful import Api
from app.models import db, tokenblocklist, users
from flask_jwt_extended import JWTManager
from app.api.resources import Register, GetUsers, Login, RefreshToken, Logout, CreateSurvey, SendAnswers, GetSurveys,\
    CompleteSurvey

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1@localhost:5432/postgres"
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
db.init_app(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(tokenblocklist.id).filter_by(jti=jti).scalar()
    return token is not None

@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    sub = jwt_data['sub']
    id = sub['id'] if type(sub) is dict else sub
    return users.get_by_id(id)

with app.app_context():
    db.create_all()

api = Api(app)
api.add_resource(Register, "/api/register/", "/api/b/register/")
api.add_resource(GetUsers, "/api/users/", "/api/users/<int:user_id>/")
api.add_resource(Login, "/api/login/", "/api/b/login/")
api.add_resource(RefreshToken, "/api/refresh/")
api.add_resource(Logout, "/api/logout/")
api.add_resource(CreateSurvey, "/api/createsurvey/")
api.add_resource(SendAnswers, "/api/completesurvey/<int:survey_id>/sendanswers/")
api.add_resource(CompleteSurvey, "/api/completesurvey/<int:survey_id>/")
# Сделать /api/completesurvey/<int:survey_id> (Получение конкретного опроса со всеми полями и pages для его прохождения, а не просмотра и тд)
api.add_resource(GetSurveys, "/api/surveys/", "/api/surveys/<int:survey_id>/")


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=3000, host='127.0.0.1')

from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1@localhost:5432/postgres"
api = Api()
db = SQLAlchemy(app)

class users(db.Model):
    def __init__(self, login, password, email, role):
        self.login = login
        self.password = password
        self.email = email
        self.role = role

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(1), nullable=False)

parser = reqparse.RequestParser()
parser.add_argument("login", type=str)
parser.add_argument("password", type=str)
parser.add_argument("email", type=str)
parser.add_argument("role", type=str)

loginParser = reqparse.RequestParser()
loginParser.add_argument("login", type=str)
loginParser.add_argument("password", type=str)

class Register(Resource):
    def post(self):
        try:
            user = parser.parse_args()
            user["password"] = generate_password_hash(user["password"])
            new_user = users(login=user["login"], password=user["password"],
                             email=user["email"], role=user["role"])
            db.session.add(new_user)
            db.session.commit()
            return {"message": "user created"}, 201
        except Exception as e:
            abort(500, "user registering error")

api.add_resource(Register, "/api/register/", "/api/b/register/")
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
api.add_resource(GetUsers,'/api/users/')

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
api.add_resource(Login, "/api/login/", "/api/b/login/")
api.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=3000, host='127.0.0.1')

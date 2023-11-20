from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
import psycopg2
import flask_sqlalchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = "cd95f3f94e2408752b114b009329aa39ca91aeed"
api = Api()

users = {}

class Register(Resource):
    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("login", type=str)
        parser.add_argument("password", type=int)
        parser.add_argument("role", type=str)
        parser.add_argument("email", type=str)
        users[user_id] = parser.parse_args()
        return users

api.add_resource(Register,'/api/register/<int:user_id>/')

class RegisterBusiness(Resource):
    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("login", type=str)
        parser.add_argument("password", type=int)
        parser.add_argument("role", type=str)
        parser.add_argument("email", type=str)
        users[user_id] = parser.parse_args()
        return users

api.add_resource(RegisterBusiness,'/api/b/register/<int:user_id>/')

class Login(Resource):
    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("login", type=str)
        parser.add_argument("password", type=int)
        users[user_id] = parser.parse_args()
        return users
api.add_resource(Login, '/api/login/<int:user_id>/')

class LoginBusiness(Resource):
    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("login", type=str)
        parser.add_argument("password", type=int)
        users[user_id] = parser.parse_args()
        return users

api.add_resource(LoginBusiness, '/api/b/login/<int:user_id>/')
api.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=3000, host='127.0.0.1')

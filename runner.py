from flask import Flask, render_template
from flask_restful import Api
from app.models import db
from app.api.resources import Register, GetUsers, Login

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1@localhost:5432/postgres"
db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)
api.add_resource(Register, "/api/register/", "/api/b/register/")
api.add_resource(GetUsers, "/api/users/")
api.add_resource(Login, "/api/login/", "/api/b/login/")

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=3000, host='127.0.0.1')

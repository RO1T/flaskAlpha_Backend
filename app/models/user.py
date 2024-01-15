from app.config.db import db


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)


class Users(db.Model):
    def __init__(self, login, hash_password, role):
        self.login = login
        self.hash_password = hash_password
        self.role = role

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    hash_password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(1), nullable=False)
    survey = db.relationship("Surveys", backref="users")
    profile = db.relationship("Profiles", backref="users")

    @property
    def loginGetter(self):
        return self.login

    @classmethod
    def get_by_id(self, id):
        return id


class Profiles(db.Model):
    def __init__(self, username, avatar_url, user_id, description):
        self.username = username
        self.avatar_url = avatar_url
        self.description = description
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    username = db.Column(db.String(), nullable=False)
    avatar_url = db.Column(db.String(), nullable=True)
    balance = db.Column(db.Integer, default=0)
    complete_survey = db.Column(db.Integer, nullable=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

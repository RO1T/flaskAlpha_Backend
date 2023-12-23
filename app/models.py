from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

db = SQLAlchemy()

class tokenblocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)

class users(db.Model):
    def __init__(self, login, hash_password, email, role):
        self.login = login
        self.hash_password = hash_password
        self.email = email
        self.role = role

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    hash_password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(1), nullable=False)
    survey = db.relationship("surveys", backref="users")
    profile = db.relationship("profiles", backref="users")

    @classmethod
    def get_by_id(self, id):
        return id

class profiles(db.Model):
    def __init__(self, username, avatar_url, user_id):
        self.username = username
        self.avatar_url = avatar_url
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    avatar_url = db.Column(db.String(), nullable=True)
    balance = db.Column(db.Integer, default=0)
    complete_survey = db.Column(db.Integer, nullable=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class surveys(db.Model):
    def __init__(self, title, description, logoPosition, value, pages, user_id):
        self.title = title
        self.description = description
        self.logoPosition = logoPosition
        self.value = value
        self.pages = pages
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    logoPosition = db.Column(db.String())
    value = db.Column(db.Integer, nullable=False)
    date_creation = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    pages = db.Column(ARRAY(JSONB), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    page = db.relationship("pages", backref="surveys")

class pages(db.Model):
    def __init__(self, name, elements, surveys_id):
        self.name = name
        self.elements = elements
        self.surveys_id = surveys_id

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    elements = db.Column(ARRAY(JSONB), nullable=False)
    surveys_id = db.Column(db.Integer, db.ForeignKey("surveys.id"))
    question = db.relationship("questions", backref="pages")

class questions(db.Model):
    def __init__(self, type, name, isRequired, title, placeholder, choices, page_id):
        self.type = type
        self.name = name
        self.isRequired = isRequired
        self.title = title
        self.placeholder = placeholder
        self.choices = choices
        self.page_id = page_id

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    isRequired = db.Column(db.Boolean(), nullable=True)
    title = db.Column(db.String(), nullable=True)
    placeholder = db.Column(db.String(), nullable=True)
    choices = db.Column(ARRAY(db.String()), nullable=True)
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))
    answer = db.relationship("answers", backref="questions")

    def serialize(self):
        fields = ["_sa_instance_state", "id", "page_id"]
        return {k: v for k, v in self.__dict__.items() if v != None and k not in fields}

class answers(db.Model):
    def __init__(self, title, answer, question_id, user_id):
        self.title = title
        self.answer = answer
        self.question_id = question_id
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))



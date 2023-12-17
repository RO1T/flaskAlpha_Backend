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

    @classmethod
    def get_by_id(self, id):
        return id

class surveys(db.Model):
    def __init__(self, title, description, logoPosition, date_creation, pages, user_id):
        self.title = title
        self.description = description
        self.logoPosition = logoPosition
        self.date_creation = date_creation
        self.pages = pages
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    logoPosition = db.Column(db.String())
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
    def __init__(self, type, name, isRequied, title, placeholder, choice):
        self.type = type
        self.name = name
        self.isRequied = isRequied
        self.title = title
        self.placeholder = placeholder
        self.choice = choice

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    isRequied = db.Column(db.Boolean(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    placeholder = db.Column(db.String(), nullable=False)
    choice = db.Column(ARRAY(db.String()), nullable=True)
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))



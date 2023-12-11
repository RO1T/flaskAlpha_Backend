from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

db = SQLAlchemy()

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

class surveys(db.Model):
    def __init__(self, title, description, logoPosition, date_creation, pages):
        self.title = title
        self.description = description
        self.logoPosition = logoPosition
        self.date_creation = date_creation
        self.pages = pages

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    logoPosition = db.Column(db.String())
    date_creation = db.Column(db.Date(), nullable=False)
    pages = db.Column(ARRAY(JSONB), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



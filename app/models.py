from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

db = SQLAlchemy()

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
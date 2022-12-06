from ..database.db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    username = db.Column(db.String(40))
    email = db.Column(db.String(60))
    password = db.Column(db.String(20))
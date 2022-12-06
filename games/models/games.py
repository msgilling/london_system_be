from ..database.db import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    min_players = db.Column(db.Integer)
    max_players = db.Column(db.Integer)
    min_age = db.Column(db.Integer)
    year = db.Column(db.Integer)
    description = db.Column(db.String(400))
    video_link = db.Column(db.String(200))
    image = db.Column(db.String(200))
    genre = db.Column(db.String(40))
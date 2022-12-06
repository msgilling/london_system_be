from games import db
from games.models.games import Game
from games.models.users import User
from games import app

#clear it all out
with app.app_context():
    db.drop_all()

#Set it back up
    db.create_all()
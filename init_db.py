from games import db
from games.models.games import Game
from games.models.users import User
from games import app
from games.database.games import games
from games.database.users import users

#clear it all out
with app.app_context():
    db.drop_all()

#Set it back up
    db.create_all()
    for gData in games:
        new_game = Game(name=gData["name"], min_players=gData["min_players"], max_players=gData["max_players"], min_age=gData["min_age"], year=gData["year"], description=gData["description"], video_link=gData["video_link"], image=gData["image"], genre=gData["genre"])
        db.session.add(new_game)
        db.session.commit()
    for new_user in users:
        new_user_created = User(name=new_user["name"], username=new_user["username"], email=new_user["email"], password=new_user["password"])
        db.session.add(new_user_created)
        db.session.commit()
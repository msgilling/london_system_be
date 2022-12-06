from flask import Blueprint, request, jsonify
from ..models.games import Game
from ..database.db import db
from werkzeug.exceptions import BadRequest
game_routes = Blueprint("game_routes", __name__)

@game_routes.route("/games", methods=["GET", "POST"])
def games_handler():
    if request.method == "GET":
        games = Game.query.all()
        outputs = map(lambda g: {"name": g.name, "min_players": g.min_players,"max_players": g.max_players,"min_age": g.min_age,"year": g.year,"description": g.description,"video_link": g.video_link,"image": g.image,"genre": g.genre}, games)
        return jsonify(list(outputs)), 200
    elif request.method == "POST":
        try:
            gData = request.json
            new_game = Game(name=gData["name"], min_players=gData["min_players"], max_players=gData["max_players"], min_age=gData["min_age"], year=gData["year"], description=gData["description"], video_link=gData["video_link"], image=gData["image"], genre=gData["genre"])
            db.session.add(new_game)
            db.session.commit()
            return jsonify(gData), 201
        except:
            return BadRequest("Sorry, failed to add game!")

@game_routes.route("/games/<int:id>", methods=["GET", "DELETE"])
def game_handler(id):
    if request.method == "GET":
        try:
            return next(game for game in games if game["id"] == id)
        except:
            return BadRequest(f"Sorry, we don't have the game: {id}!")
    elif request.method == "DELETE":
        try:
            del games[id - 1]
            return jsonify(games), 204
        except:
            raise BadRequest(f"Failed to delete game: {id}!")

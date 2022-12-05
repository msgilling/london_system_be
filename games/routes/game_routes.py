from flask import Blueprint, request, jsonify
from ..database.games import games
from werkzeug.exceptions import BadRequest
game_routes = Blueprint("game_routes", __name__)

@game_routes.route("/games", methods=["GET", "POST"])
def games_handler():
    if request.method == "GET":
        return jsonify(games), 200
    elif request.method == "POST":
        new_game = request.json
        last_id = games[-1]["id"]
        new_game["id"] = last_id + 1
        games.append(new_game)
        return new_game, 201

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

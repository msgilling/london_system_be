from flask import Blueprint, request, jsonify
from ..database.games import games
from werkzeug.exceptions import BadRequest
user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/login", methods=["GET", "POST"])
def login_handler():
    return "Login"

from flask import Flask, jsonify, request, render_template
from .models.users import User
from werkzeug.exceptions import NotFound, InternalServerError, MethodNotAllowed, BadRequest
from .routes.game_routes import game_routes
from .routes.user_routes import user_routes
from flask_login import LoginManager
from flask_cors import CORS

#db stuff
from dotenv import load_dotenv
from os import environ
from .database.db import db

#load env variables
load_dotenv()
database_uri = environ.get("DATABASE_URL")

app = Flask( __name__ )
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'),
    SECRET_KEY="hellothere"
)
CORS(app)
db.app = app
db.init_app(app)

app.register_blueprint(game_routes)
app.register_blueprint(user_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/")
def welcome():
    return "Welcome to London System!"

@app.errorhandler(NotFound)
def handle_404(err):
    return jsonify({"message": f"Oops {err}"}), 404
    
@app.errorhandler(InternalServerError)
def handle_500(err):
    return jsonify({"message": f"Oops, it's not you, it's us."}), 500

@app.errorhandler(MethodNotAllowed)
def handle_405(err):
    return jsonify({"message": f"Oops {err}"}), 405

if __name__ == "__main__":
    app.run(debug=True)

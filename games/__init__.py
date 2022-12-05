from flask import Flask, jsonify, request, render_template
from .database.users import users
from werkzeug.exceptions import NotFound, InternalServerError, MethodNotAllowed, BadRequest
from .routes.game_routes import game_routes
from .routes.user_routes import user_routes
from flask_login import LoginManager

app = Flask( __name__ )

app.register_blueprint(game_routes)
app.register_blueprint(user_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return next(user for user in users if user["id"] == id)

@app.route("/")
def welcome():
    return "Welcome to London System!"

# @app.route("/login")
# def login():
#     return "Login"


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

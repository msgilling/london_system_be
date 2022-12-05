from flask import Blueprint, request, jsonify
from ..database.users import users
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/login", methods=["GET", "POST"])
def login_handler():
    if request.method == "GET":
        return jsonify(users), 200
    elif request.method == "POST":
        new_user_email = request.json.get("email")
        new_user_password = request.json.get("password")
        found_user = next(user for user in users if user["email"] == new_user_email)
        if found_user:
            if check_password_hash(found_user["password"], new_user_password):
                login_user(found_user, remember=True)
                return "Logged in!", 200
            else:
                return "Password is incorrect", 400
        else:
            return "email is incorrect", 400

@user_routes.route("/sign-up", methods=["GET", "POST"])
def sign_up_handler():
    if request.method == "GET":
        return jsonify(users), 200
    elif request.method == "POST":
        new_user = request.json
        try :
            foundUserEmail = next(y for y in users if y["email"] == new_user["email"])
        except:
            foundUserEmail = False
        try: 
            foundUserUsername = next(x for x in users if x["username"] == new_user["username"])
        except:
            foundUserUsername = False
        if foundUserEmail:
            return 'user already exists', 400
        if foundUserUsername:
            return 'user already exists', 400
        elif new_user["password1"] != new_user["password2"]:
            return "passwords don't match", 400
        else:
            last_id = users[-1]["id"]
            new_user["id"] = last_id + 1
            new_user["password"] = generate_password_hash(new_user["password1"], method='sha256')
            users.append(new_user)
            login_user(new_user, remember=True)
            return new_user, 201

@user_routes.route("/logout")
@login_required
def logout_handler():
    logout_user()
    return "logout"
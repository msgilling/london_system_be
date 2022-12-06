from flask import Blueprint, request, jsonify
from ..models.users import User
from ..database.db import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/login", methods=["GET", "POST"])
def login_handler():
    if request.method == "GET":
        users = User.query.all()
        outputs = map(lambda g: {"username": g.username, "name": g.name,"email": g.email,"password": g.password}, users)
        return jsonify(list(outputs)), 200
    elif request.method == "POST":
        new_user_email = request.json.get("email")
        new_user_password = request.json.get("password")
        foundUserEmail = User.query.filter_by(email=str(new_user_email)).first() 
        if foundUserEmail:
            if check_password_hash(foundUserEmail.password, new_user_password):
                login_user(foundUserEmail, remember=True)
                return "Logged in!", 200
            else:
                return BadRequest(f"Failed login! Password incorrect")
        else:
            return BadRequest(f"Failed login! email incorrect")

@user_routes.route("/sign-up", methods=["GET", "POST"])
def sign_up_handler():
    if request.method == "GET":
        users = User.query.all()
        outputs = map(lambda g: {"username": g.username, "name": g.name,"email": g.email,"password": g.password}, users)
        return jsonify(list(outputs)), 200
    elif request.method == "POST":
        new_user = request.json
        try :
            foundUserEmail = User.query.filter_by(email=str(new_user["email"])).first() 
        except:
            foundUserEmail = False
        try: 
            foundUserUsername = User.query.filter_by(username=str(new_user["username"])).first()
        except:
            foundUserUsername = False
        if foundUserEmail:
            print(foundUserEmail)
            return 'user already exists', 400
        if foundUserUsername:
            return 'user already exists', 400
        elif new_user["password1"] != new_user["password2"]:
            return "passwords don't match", 400
        else:
            new_user["password"] = generate_password_hash(new_user["password1"], method='sha256')
            new_user_created = User(name=new_user["name"], username=new_user["username"], email=new_user["email"], password=new_user["password"])
            db.session.add(new_user_created)
            db.session.commit()
            login_user(new_user_created, remember=True)
            return jsonify(new_user), 201

@user_routes.route("/logout")
@login_required
def logout_handler():
    logout_user()
    return "logout"
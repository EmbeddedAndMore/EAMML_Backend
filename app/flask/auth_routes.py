from dataclasses import dataclass
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, request, current_app, abort
from flask_httpauth import HTTPTokenAuth
from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import UserAlreadyExists
from ..controller import user_mgmt


auth_route = Blueprint("auth_route", __name__, url_prefix="/auth")

token_auth = HTTPTokenAuth(scheme="Bearer")


@token_auth.verify_token
def verify_token(token):
    try:
        decoded_jwt = jwt.decode(
            token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
    except Exception as ex:
        return None
    return decoded_jwt


def generate_token(username: str):
    return jwt.encode(
        {"user": username, "exp": datetime.utcnow() + timedelta(minutes=30)},
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )


@auth_route.route("/signup", methods=["POST"])
def signup():
    try:
        username = user_mgmt.register(request.json)
        token = generate_token(username)
    except ValueError:
        abort(400)
    except UserAlreadyExists:
        return jsonify(result="User already exists."), 409
    except SQLAlchemyError:
        abort(400)
    return jsonify(result={"token": token}), 200


@auth_route.route("/signin", methods=["POST"])
def signin():

    try:
        username = user_mgmt.login(request.json)
        token = generate_token(username=username)
    except ValueError:
        return jsonify(result="Username or password is wrong."), 401
    return jsonify(result={"token": token}), 200

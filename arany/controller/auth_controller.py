from flask import Blueprint, request
from werkzeug.wrappers import Response
from .utils import validated_request_body
from arany.model.dto import UserDTO
from arany.service import UserService

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["POST"])
@validated_request_body(UserDTO)
def login():
    username = request.get_json()["username"]
    return {"message": f"user {username} logged in successfully"}


@bp.route("/logout", methods=["GET"])
def logout():
    username = request.get_json()["username"]
    return {"message": f"user {username} logged out successfully"}


@bp.route("/register", methods=["POST"])
@validated_request_body(UserDTO)
def register():
    username = request.get_json()["username"]
    return {"message": f"user {username} registered successfully"}

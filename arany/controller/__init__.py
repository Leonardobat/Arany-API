from flask import Blueprint
from .auth_controller import bp as auth_bp
from .controller import UsersController

users_bp = UsersController().blueprint
index_bp = Blueprint("index", __name__, url_prefix="/")


@index_bp.route("")
def index():
    return {"message": "read the OpenApi to discover the api routes"}

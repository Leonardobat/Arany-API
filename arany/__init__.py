from flask import Flask
from os import environ
from arany.controller import auth_bp, index_bp, users_bp
from arany.errorhandler import ErrorHandler
from arany.model import db


def create_app(test_config=None) -> Flask:

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=environ.get("DATABASE_URL", "sqlite:///project.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DRY_RUN_DB=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():

        app.register_blueprint(auth_bp)
        app.register_blueprint(index_bp)
        app.register_blueprint(users_bp)
        app.register_error_handler(400, ErrorHandler.invalid_json_body)

        if not (app.config["DRY_RUN_DB"]):
            db.create_all()

        return app

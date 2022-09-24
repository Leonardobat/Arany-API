from flask.views import MethodView
from .utils import validated_request_body
from arany.model.dto import UserDTO
from arany.service import UserService, ModelService
from flask import Blueprint, request, jsonify, Response
from arany.model import User
from flask_sqlalchemy import Pagination


class UsersController:
    blueprint = Blueprint("user", __name__, url_prefix="/users")
    init_every_request = False

    def __init__(self, service: ModelService = UserService()):
        self.service = service
        self.blueprint.add_url_rule(f"/", view_func=self.get_paginated, methods=["GET"])
        self.blueprint.add_url_rule(f"/<int:id>", view_func=self.get, methods=["GET"])
        self.blueprint.add_url_rule(
            f"/<int:id>", view_func=self.patch, methods=["PATCH"]
        )
        self.blueprint.add_url_rule(
            f"/<int:id>", view_func=self.delete, methods=["DELETE"]
        )
        self.blueprint.add_url_rule(f"/", view_func=self.post, methods=["POST"])

    def get_paginated(self):
        page = request.args.get("page", type=int, default=None)
        per_page = request.args.get("per_page", type=int, default=None)
        users_page = self.service.get_paginated(page, per_page)
        return self.page_to_json(users_page)

    def get(self, id: int):
        user = self.service.get(id)
        return self.jsonify_dto(user)

    @validated_request_body(UserDTO)
    def post(self):
        self.service.add(request.get_json())
        return self.jsonify_dto(user)

    @validated_request_body(UserDTO)
    def patch(self, id: int):
        dto = UserDTO.from_json(request.get_json())
        user = self.service.update(id, dto)
        return self.jsonify_dto(user)

    def delete(self, id: int):
        self.service.delete(id)
        return jsonify({"message": f"User {id} deleted"})

    @staticmethod
    def to_dto(user: User) -> UserDTO:
        return UserDTO(user.username, user.password)

    @staticmethod
    def jsonify_dto(user: User) -> Response:
        return jsonify(UsersController.to_json(user))

    @staticmethod
    def to_json(user: User) -> dict:
        return UsersController.to_dto(user).to_dict()

    @staticmethod
    def page_to_json(page: Pagination) -> dict:
        return {
            "page": page.page,
            "per_page": page.per_page,
            "total": page.total,
            "items": list(map(UsersController.to_json, page.items)),
        }

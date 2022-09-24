from http import HTTPStatus
from random import randrange
from arany.controller.controller import UsersController
from arany.service import UserService
from arany.model import User
from arany.model.dto import UserDTO
from flask_sqlalchemy import Pagination


class MockDB:
    @staticmethod
    def get_paginated(user: User, page: int, per_page: int):
        return Pagination(
            query="test",
            items=[user],
            page=page,
            per_page=per_page,
            total=1,
        )

    @staticmethod
    def get(user: User):
        return user

    @staticmethod
    def update(mock_user: User, new_user_data: UserDTO):
        mock_user.username = new_user_data.username
        mock_user.password = new_user_data.password
        return mock_user


class TestUsersController:
    def test_get_paginated_request(self, client, monkeypatch):
        user = User(username="test", password="some", id=1)
        monkeypatch.setattr(
            UserService,
            "get_paginated",
            lambda _, page, per_page: MockDB.get_paginated(user, page, per_page),
        )

        response = client.get(f"/users/")

        expected_response = [UsersController.to_json(user)]
        expected_status_code = HTTPStatus.OK

        assert expected_status_code == response.status_code
        assert expected_response == response.get_json()["items"]

    def test_get_request(self, client, monkeypatch):
        user = User(username="test", password="some", id=1)
        monkeypatch.setattr(UserService, "get", lambda _, id: MockDB.get(user))

        response = client.get(f"/users/{user.id}")

        expected_response = UsersController.to_json(user)
        expected_status_code = HTTPStatus.OK

        assert expected_status_code == response.status_code
        assert expected_response == response.get_json()

    def test_delete_request(self, client, monkeypatch):
        user = User(username="test", password="some", id=1)
        monkeypatch.setattr(UserService, "delete", lambda _, id: MockDB.get(user))

        response = client.delete(f"/users/{user.id}")

        expected_response = {"message": f"User {user.id} deleted"}
        expected_status_code = HTTPStatus.OK

        assert expected_status_code == response.status_code
        assert expected_response == response.get_json()

    def test_patch_request(self, client, monkeypatch):
        user = User(username="test", password="some", id=1)
        new_user_data = UserDTO("test", "value")
        monkeypatch.setattr(UserService, "get", lambda _, id: MockDB.get(user))
        monkeypatch.setattr(
            UserService,
            "update",
            lambda _, id, new_data: MockDB.update(user, new_data),
        )

        response = client.patch(f"/users/{user.id}", json=new_user_data.to_dict())

        expected_response = new_user_data.to_dict()
        expected_status_code = HTTPStatus.OK

        assert expected_status_code == response.status_code
        assert expected_response == response.get_json()

from arany.model import db, User
from arany.service import UserService
from arany.model.dto import UserDTO
from sqlalchemy import select
import pytest


class TestUserService:
    service: UserService = UserService()

    def test_get(self, app_ctx):
        mock_user = User(username="Teste", password="123")
        db.session.add(mock_user)
        db.session.commit()

        result = self.service.get(mock_user.id)
        assert result == mock_user

    def test_add(self, app_ctx):
        mock_user = UserDTO(username="Teste", password="123")

        value = self.service.add(mock_user)
        result = db.session.scalars(
            select(User).where(User.username == mock_user.username)
        ).first()
        assert result.username == mock_user.username
        assert result.password == mock_user.password

    def test_delete(self, app_ctx):
        mock_user = User(username="Teste", password="123")
        db.session.add(mock_user)
        db.session.commit()

        self.service.delete(mock_user.id)
        result = db.session.scalars(select(User).where(User.id == mock_user.id)).first()
        assert result == None

    def test_update(self, app_ctx):
        mock_dto = UserDTO(username="NewName", password="123")
        mock_user = User(username="OldName", password="123")
        db.session.add(mock_user)
        db.session.commit()

        result = self.service.get(mock_user.id)
        assert result == mock_user

from arany.model import db, User
from arany.model.dto import UserDTO
from sqlalchemy import select
from sqlalchemy.orm.scoping import scoped_session
from abc import ABC, abstractmethod
from flask_sqlalchemy import Pagination


class ModelService(ABC):
    @abstractmethod
    def add(self, item_dto):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_paginated(self, page, per_page) -> Pagination:
        pass

    @abstractmethod
    def update(self, id, dto):
        pass

    @abstractmethod
    def delete(self, item_dto):
        pass


class UserService(ModelService):
    def __init__(self, session: scoped_session = db.session):
        self.session = session

    def get(self, id: int) -> User:
        return self.session.scalars(select(User).where(User.id == id)).first()

    def get_paginated(self, page: int = None, per_page: int = None) -> Pagination:
        return User.query.order_by(User.id).paginate(page, per_page)

    def add(self, dto: UserDTO) -> User:
        user = User(username=dto.username, password=dto.password)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, id: int, dto: UserDTO) -> User:
        user = self.get(id)
        user.password = dto.password
        user.username = dto.username
        self.session.commit()
        return user

    def delete(self, id: int):
        user = self.get(id)
        self.session.delete(user)
        self.session.commit()

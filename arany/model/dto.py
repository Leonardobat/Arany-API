from abc import ABC, abstractmethod
import json


class RequestBodyDTO(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def schema() -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_json(raw_json: dict):
        pass

    @staticmethod
    @abstractmethod
    def is_valid_json(raw_json: str) -> bool:
        pass


class UserDTO(RequestBodyDTO):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_dict(self) -> dict:
        return {"username": self.username, "password": self.password}

    @staticmethod
    def schema():
        return {"username": "", "password": ""}

    @staticmethod
    def from_json(raw_json: dict):
        if UserDTO.is_valid_json(raw_json):
            return UserDTO(raw_json["username"], raw_json["password"])
        else:
            return None

    @staticmethod
    def is_valid_json(decoded_json: dict) -> bool:
        if "username" in decoded_json.keys() and "password" in decoded_json.keys():
            return isinstance(decoded_json["username"], str) and isinstance(
                decoded_json["password"], str
            )
        else:
            return False

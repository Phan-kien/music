from abc import ABC, abstractmethod
from .User_object import User
from .User_interface import RegisterInput, LoginInput, UserOutput

class UserDAOInterface(ABC):

    @abstractmethod
    def create_user(self, input_data: RegisterInput) -> User:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def verify_user_credentials(self, input_data: LoginInput) -> User:
        pass

    @abstractmethod
    def store_token(self, user_id: int, token: str) -> bool:
        pass

    @abstractmethod
    def clear_token(self, user_id: int) -> bool:
        pass

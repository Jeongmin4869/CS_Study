from app.application.interface.user_repository import AbstractRepository
from app.domain.entity import User


class UserService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def create_user(self, user_name: str):
        # 데이터베이스 저장
        _user = User(name=user_name)
        if self.repository.find_one(model=_user):
            raise ValueError("유저가 이미 존재한다")
        user = self.repository.create(_user)

        return user

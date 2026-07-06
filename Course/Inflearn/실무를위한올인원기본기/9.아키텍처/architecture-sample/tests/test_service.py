import pytest

from app.application.service.user_service import UserService
from app.domain.entity import User
from tests.fakes import FackUserRepository


@pytest.fixture  # 테스트 함수 수행 전 사전 시행
def user_service():
    repository = FackUserRepository()
    user_service = UserService(repository=repository)
    return user_service


def test_create_user_well(user_service):
    user_name = "grab"
    user = user_service.create_user(user_name=user_name)
    assert user == User(name=user_name)


def test_create_user_duplicated(user_service):
    user_name = "grab"
    user_service.create_user(user_name=user_name)

    # 중복가입
    with pytest.raises(ValueError):
        user_service.create_user(user_name=user_name)

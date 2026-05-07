import pytest
from main import GrabStore, Product, User


@pytest.fixture(scope="function") # 테스트함수 호출 시 한번씩 호출
def grab_store():
    return  GrabStore(
        products={
            1: Product(name="키보드", price=30000),
            2: Product(name="컴퓨터", price=5000000),
        }
    )


@pytest.fixture(scope="function")
def user(grab_store):
    return User(money=100000, store=grab_store)
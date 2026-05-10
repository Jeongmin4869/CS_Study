import pytest

from GrabRealStore import GrabRealStore
from main import GrabStore, Product, User

API_URL = "https://fakestoreapi.com/products"

@pytest.fixture(scope="function")
def mock_products():
    return  {
        1:{"title":"키보드", "price":30000},
        2:{"title":"컴퓨터", "price":5000000},
    }

@pytest.fixture(scope="function")
def mock_api(requests_mock, mock_products):
    mock_product1 = mock_products[1]
    mock_product2 = mock_products[2]

    #mocking
    requests_mock.get(f"{API_URL}/1", json=mock_product1)
    requests_mock.get(f"{API_URL}/2", json=mock_product2)
    requests_mock.delete(f"{API_URL}/1", json=mock_product1)
    requests_mock.delete(f"{API_URL}/2", json=mock_product2)

@pytest.fixture(scope="function") # 테스트함수 호출 시 한번씩 호출
def grab_store():
    return GrabRealStore()

@pytest.fixture(scope="function")
def user(grab_store):
    return User(money=100000, store=grab_store)
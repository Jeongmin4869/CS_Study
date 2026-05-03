# 1번. Store의 확장성
# 개선점
# - 1. Store를 추상화
# - 2. 의존성 주입을 한다.

# 2번. Store에 있는 상품과 돈을 마음대로 접근할 수 있다.
# 개선점
# - 1. Store의 책임을 정의하고 캡슐화
# - 2. User의 결재 로직을 수정
# - 3. User 캡슐화

# 3번. User가 많은 행위를 책임지고 있다.
# 개선점
# - 1. 상점에서 상품을 판매하는 행위를 추상화하고 구체적인 로직을 해당 메소드로 옮긴다.

# 4번. Product가 책임을 가져야 한다.
# 개선점
# - 1. 딕셔너리 타입을 클래스(데이터 클래스) 객체로 변환한다.

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int

class Store(ABC): # 추상화
    @abstractmethod
    def __init__(self):
        self._money = 0
        self.name = ""
        self._products = {}

    @abstractmethod
    def show_product(self, product_id):
        pass

    @abstractmethod
    def sell_product(self, product_id, money):
        pass


class GrabStore(Store):
    def __init__(self, products):
        self._money = 0
        self.name = "그랩마켓"
        self._products = products

    def set_money(self, money):
        self._money = money

    def set_products(self, products):
        self._products = products

    def show_product(self, product_id):
        return self._products[product_id]

    def sell_product(self, product_id, money):
        #validation 코드 최소화
        product = self.show_product(product_id=product_id)
        if not product:
            return Exception("상품이 존재하지 않습니다")

        self._take_money(money=money)
        try:
            _product = self._take_out_product(product_id=product_id)
        except Exception as e:
            self._return_money(money=money)
            raise e
        return _product

    def _take_out_product(self, product_id):
        return self._products.pop(product_id)

    def _take_money(self, money):
        self._money += money

    def _return_money(self, money):
        self._money -= money

class User:
    def __init__(self, money, store: Store):
        self._money = money
        self.store = store #의존성주입
        self.belongs = []

    def get_money(self):
        return self._money

    def get_belongs(self):
        return self.belongs

    def get_store(self):
        return self.store

    def see_product(self, product_id):
        product = self.store.show_product(product_id=product_id)
        return product

    def purchase_product(self, product_id):
        product = self.see_product(product_id=product_id)
        price = product.price
        if self._check_money(money=price):
            self._give_money(money=price)
            try:
                my_product = self.store.sell_product(product_id=product_id, money=price)
                self._add_belong(my_product)
                return my_product
            except Exception as e:
                self._take_money(money=price)
                print(f"구매중 문제가 발생하였습니다 {str(e)}")

        else:
            raise Exception("잔돈이 부족합니다")

    def _check_money(self, money):
        return self._money >= money

    def _give_money(self, money):
        self._money -= money

    def _take_money(self, money):
        self._money += money

    def _add_belong(self, product):
        self.belongs.append(product) # List에 값 추가


if __name__ == "__main__":
    store = GrabStore(
        products={
            1:Product(name="키보드", price=30000),
            2:Product(name="컴퓨터", price=50000),
        }
    )

    user = User(money=100000, store=store)
    user.purchase_product(product_id=1)
    print(f"user의 잔돈 : {user.get_money()}")
    print(f"user가 구매한 상품 : {user.get_belongs()}")



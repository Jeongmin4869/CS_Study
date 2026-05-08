from main import Store, Product
import requests
#using fake api

class GrabRealStore(Store):
    def __init__(self, url="https://fakestoreapi.com"):
        self._money = 0
        self.name = "그랩마켓"
        self.url = url

    def set_money(self, money):
        self._money = money

    def show_product(self, product_id):
        # request : 외부 웹서버와 통신하기 위해 사용하는 모델
        res = requests.get(f"{self.url}/products/{product_id}")
        product = res.json()
        return Product(name=product["title"], price=product["price"])

    def sell_product(self, product_id, money):
        #validation 코드 최소화
        product = self.show_product(product_id=product_id)
        if not product:
            raise Exception("상품이 존재하지 않습니다")

        self._take_money(money=money)
        try:
            _product = self._take_out_product(product_id=product_id)
        except Exception as e:
            self._return_money(money=money)
            raise e
        return _product

    def _take_out_product(self, product_id):
        res = requests.delete(f"{self.url}/products/{product_id}")
        product = res.json()
        return Product(name=product["title"], price = product["price"])

    def _take_money(self, money):
        self._money += money

    def _return_money(self, money):
        self._money -= money

if __name__=="__main__":
    store = GrabRealStore()
    result = store.show_product(product_id=1)
    print(result)
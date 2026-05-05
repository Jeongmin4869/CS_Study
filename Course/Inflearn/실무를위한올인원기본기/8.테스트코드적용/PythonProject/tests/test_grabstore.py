from main import GrabStore, Product


def test_show_product(grab_store):
    #given
    product_id = 1

    #when
    product = grab_store.show_product(product_id)

    #then
    assert product == Product(name="키보드", price=30000)



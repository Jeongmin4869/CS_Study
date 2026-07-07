from app.infrastructure.database.orm import db, UserModel, ProductModel

if __name__ == "__main__":

    db.init(database="database.db")
    db.connect()
    # 초기화
    UserModel.create_table()
    ProductModel.create_table()
    ProductModel.bulk_create(
        [
            ProductModel(name="키보드", price=30000),
            ProductModel(name="모니터", price=50000),
            ProductModel(name="노트북", price=200000),
        ]
    )
    db.close()

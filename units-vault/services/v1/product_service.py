from documents import Batch, Product
from use_cases import CreateProductV1


class ProductService:
    def create(self, data={}):
        CreateProductV1(
            batch_document=Batch,
            product_document=Product,
            product_data=data
        ).start()

from documents import Product, Batch
from repositories import ProductRepository, BatchRepository


class ProductService:
    def __init__(self):
        self.repository = ProductRepository(product_document=Product)
        self.batch_repository = BatchRepository(batch_document=Batch)

    def create(self, data={}):
        batch = self.batch_repository.get(filter={'reference': data['batch']})

        data['batch'] = batch.pk

        self.repository.create(data=data)

    def delete(self, bar_code: str):
        product = self.repository.get(filter={'bar_code': bar_code})

        self.repository.delete(product=product)

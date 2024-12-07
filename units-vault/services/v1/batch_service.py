from documents import Batch, Store, Product
from repositories import BatchRepository, StoreRepository, ProductRepository


class BatchService:
    def __init__(self):
        self.store_repository = StoreRepository(store_document=Store)
        self.product_repository = ProductRepository(product_document=Product)
        self.repository = BatchRepository(batch_document=Batch)

    def create(self, data={}):
        store = self.store_repository.get(filter={
            'unit': data.get('store_unit')
        })

        self.repository.create(data={
            "expiry_date": data.get('expiry_date'),
            "inserction_datetime": data.get('inserction_datetime'),
            "supplier_document": data.get('supplier_document'),
            "reference": data.get('reference'),
            "store": store.pk
        })

    def delete(self, reference: str):
        batch = self.repository.get(filter={
            'reference': reference
        })

        product = self.product_repository.get(
            filter={'batch': batch.pk},
            can_raises=False
        )

        if product:
            self.product_repository.delete(product)

        self.repository.delete(batch)

    def get(self, reference: str) -> Batch:
        return self.repository.get(filter={
            'reference': reference
        })

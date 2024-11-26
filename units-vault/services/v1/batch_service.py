from documents import Batch, Store
from repositories import BatchRepository, StoreRepository


class BatchService:
    def __init__(self):
        self.store_repository = StoreRepository(store_document=Store)
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

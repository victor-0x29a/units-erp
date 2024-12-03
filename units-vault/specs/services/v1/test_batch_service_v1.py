import pytest
from services.v1.batch_service import BatchService
from repositories import StoreRepository, ProductRepository, BatchRepository
from documents import Store, Product, Batch
from datetime import timedelta
from utils.dates import get_now
from exceptions import MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.constants import company_doc


class TestCreateBatch:
    def test_should_create(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        service = BatchService()

        create_payload = {
            "reference": "REFERER001",
            "inserction_datetime": get_now(),
            "expiry_date": get_now() + timedelta(days=1),
            "store_unit": 1,
            "supplier_document": company_doc
        }

        service.create(data=create_payload)


class TestDeleteBatch:
    def test_should_delete(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        service = BatchService()

        create_payload = {
            "reference": "REFERER001",
            "inserction_datetime": get_now(),
            "expiry_date": get_now() + timedelta(days=1),
            "store_unit": 1,
            "supplier_document": company_doc
        }

        service.create(data=create_payload)

        service.delete(reference=create_payload.get('reference'))

    def test_should_fails_when_unexistent_batch(self, mocker):
        service = BatchService()

        with pytest.raises(MissingDoc) as error:
            service.delete(reference="REFERER001")

        assert error.value.message == "Batch not found."

    def test_should_delete_the_product(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        product_repository = ProductRepository(product_document=Product)
        batch_repository = BatchRepository(batch_document=Batch)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch = batch_repository.create(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": company_doc,
            "reference": "REFERER001",
            "store": store.pk
        })

        product_repository.create(data={
            'batch': batch.pk,
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        })

        service = BatchService()

        service.delete(reference="REFERER001")

        with pytest.raises(MissingDoc) as error:
            batch_repository.get(filter={'reference': 'REFERER001'})

        assert error.value.message == "Batch not found."

        with pytest.raises(MissingDoc) as error:
            product_repository.get(filter={'batch': batch.pk})

        assert error.value.message == "Product not found."

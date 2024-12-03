from main import app
import pytest
from bson import ObjectId, uuid
from datetime import timedelta
from repositories import StoreRepository, BatchRepository
from documents import Batch, Store
from utils.dates import get_now, from_date_to_str
from exceptions import HasWithSameBatch, GreaterThanPrice, MissingDoc, AlreadyExists
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.constants import company_doc
from ...__mocks__.test_client import create_test_client

client = create_test_client(app)


class TestCreateProductIntegrationV1():
    def test_should_create(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch_repository.create(data={
            "supplier_document": company_doc,
            "reference": "batch00001",
            "expiry_date": get_now() + timedelta(days=2),
            "inserction_datetime": get_now(),
            "store": store.pk
        })

        response = client.post("/v1/product", json={
            "name": "Foo",
            "price": 3.45,
            "discount_value": 3.20,
            "base_stock": 310,
            "batch": "batch00001",
            "type": "construction",
            "for_use": "for_sale"
        })

        assert response.status_code == 204

    def test_should_reject_when_already_exists_with_same_batch(eslf, mocker):
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch_repository.create(data={
            "supplier_document": company_doc,
            "reference": "batch00001",
            "expiry_date": get_now() + timedelta(days=2),
            "inserction_datetime": get_now(),
            "store": store.pk
        })

        client.post("/v1/product", json={
            "name": "Foo",
            "price": 3.45,
            "discount_value": 3.20,
            "base_stock": 310,
            "batch": "batch00001",
            "type": "construction",
            "for_use": "for_sale"
        })

        with pytest.raises(HasWithSameBatch) as exception:
            client.post("/v1/product", json={
                "name": "Foo",
                "price": 3.45,
                "base_stock": 310,
                "batch": "batch00001",
                "type": "construction",
                "for_use": "for_sale"
            })

        assert exception.value.message == "Already has product with the same batch."

    def test_should_reject_when_discount_is_greater_than_price(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch_repository.create(data={
            "supplier_document": company_doc,
            "reference": "batch00002",
            "expiry_date": get_now() + timedelta(days=2),
            "inserction_datetime": get_now(),
            "store": store.pk
        })

        with pytest.raises(GreaterThanPrice) as exception:
            client.post("/v1/product", json={
                "name": "Foo",
                "price": 3.45,
                "discount_value": 4.0,
                "base_stock": 310,
                "batch": "batch00002",
                "type": "construction",
                "for_use": "for_sale"
            })

        assert exception.value.message == "The discount is greater than the price of the product."

    def test_should_reject_when_batch_unexists(self, mocker):
        with pytest.raises(MissingDoc) as exception:
            client.post("/v1/product", json={
                "name": "Foo",
                "price": 3.45,
                "discount_value": 3.20,
                "base_stock": 310,
                "batch": str(ObjectId()),
                "type": "construction",
                "for_use": "for_sale"
            })

        assert exception.value.message == "Batch not found."
        assert exception.value.code == 1003

    def test_should_reject_when_already_exists_by_bar_code(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch_data = {
            "cnpj": company_doc,
            "ref": uuid.uuid4().hex,
            "expiry_date": from_date_to_str(get_now() + timedelta(days=2)),
            "store_unit": 1
        }

        data = {
            "name": "Foo",
            "price": 3.45,
            "discount_value": 2.0,
            "base_stock": 310,
            "batch": batch_data['ref'],
            "type": "construction",
            "for_use": "for_sale",
            "bar_code": "1234567891021"
        }

        client.post("/v1/batch", json=batch_data)

        client.post("/v1/product", json=data)

        batch_data["ref"] = uuid.uuid4().hex

        client.post("/v1/batch", json=batch_data)

        data['batch'] = batch_data['ref']

        with pytest.raises(AlreadyExists) as error:
            client.post("/v1/product", json=data)

        assert error.value.message == 'Product already exists by bar code.'

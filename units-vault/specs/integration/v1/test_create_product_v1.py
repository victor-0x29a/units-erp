from main import app
import pytest
from bson import ObjectId, uuid
from datetime import timedelta
from fastapi.testclient import TestClient
from documents import Product, Batch, Store
from unittest.mock import MagicMock
from utils.dates import get_now, from_date_to_str
from exceptions import HasWithSameBatch, GreaterThanPrice, MissingDoc, UniqueKey

client = TestClient(app)


class TestCreateProductIntegrationV1():
    def test_should_create(self, mocker):
        magic_batch = MagicMock()

        magic_batch.id = "batch00001"

        mocker.patch.object(Batch, 'objects', return_value=magic_batch)

        mocker.patch.object(Product, 'objects', return_value=None)

        mocker.patch.object(Product, 'save', return_value=True)

        response = client.post("/v1/product", json={
            "name": "Foo",
            "price": 3.45,
            "base_stock": 310,
            "batch": "batch00002",
            "type": "construction",
            "for_use": "for_sale"
        })

        assert response.status_code == 204

    def test_should_reject_when_already_exists_with_same_batch(eslf, mocker):
        magic_batch = MagicMock()

        magic_batch.id = "batch00001"

        mocker.patch.object(Batch, 'objects', return_value=magic_batch)

        mocker.patch.object(Product, 'objects', return_value=True)

        mocker.patch.object(Product, 'save', return_value=True)

        with pytest.raises(HasWithSameBatch) as exception:
            client.post("/v1/product", json={
                "name": "Foo",
                "price": 3.45,
                "base_stock": 310,
                "batch": "batch00002",
                "type": "construction",
                "for_use": "for_sale"
            })

        assert exception.value.message == "Already has product with the same batch."

    def test_should_reject_when_discount_is_greater_than_price(self, mocker):
        magic_batch = MagicMock()

        magic_batch.id = "batch00001"

        mocker.patch.object(Batch, 'objects', return_value=magic_batch)

        mocker.patch.object(Product, 'objects', return_value=False)

        mocker.patch.object(Product, 'save', return_value=True)

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
        mocker.patch.object(Batch.objects, 'get', side_effect=MissingDoc('Batch not found.'))

        with pytest.raises(MissingDoc) as exception:
            client.post("/v1/product", json={
                "name": "Foo",
                "price": 3.45,
                "discount_value": 4.0,
                "base_stock": 310,
                "batch": str(ObjectId()),
                "type": "construction",
                "for_use": "for_sale"
            })

        assert exception.value.message == "Batch not found."
        assert exception.value.code == 1003

    def test_should_reject_when_already_exists_by_bar_code(self, mocker):
        magic_property = MagicMock()

        magic_property.id = ObjectId()

        magic_first = MagicMock()

        magic_first.first.return_value = magic_property

        mocker.patch.object(
            Store,
            'objects',
            return_value=magic_first
        )

        mocker.patch.object(Store, 'objects', return_value=magic_first)

        batch_data = {
            "cnpj": "59968706000194",
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

        with pytest.raises(UniqueKey) as error:
            client.post("/v1/product", json=data)

        assert error.value.message == 'Product with same bar code already exists.'

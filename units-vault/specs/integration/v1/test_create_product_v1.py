from main import app
import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from exceptions import HasWithSameBatch, GreaterThanPrice, MissingDoc
from documents import Product, Batch

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

from main import app
import pytest
from datetime import timedelta
from repositories import StoreRepository, BatchRepository, ProductRepository
from documents import Batch, Store, Product
from utils.dates import get_now
from exceptions import MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.constants import company_doc
from ...__mocks__.test_client import create_test_client

client = create_test_client(app)


class TestDeleteProductIntegrationV1():
    def test_should_delete(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)
        product_repository = ProductRepository(product_document=Product)

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

        bar_code = product_repository.get(
            filter={"name": "Foo"}
        ).bar_code

        deletion_response = client.delete(f"/v1/product/{bar_code}")

        assert deletion_response.status_code == 204

        product = product_repository.get(
            filter={"name": "Foo"},
            can_raises=False
        )

        assert not product

    def test_should_fail_when_unexists(self, mocker):
        with pytest.raises(MissingDoc) as error:
            client.delete("/v1/product/1234567891012")

        assert error.value.message == "Product not found."

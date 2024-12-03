import pytest
from datetime import datetime
from main import app
from repositories import StoreRepository, BatchRepository, ProductRepository
from documents import Batch, Store, Product
from exceptions import MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.constants import company_doc
from ...__mocks__.test_client import create_test_client

client = create_test_client(app)


class TestDeleteBatchIntegrationV1():
    def test_should_delete(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        next_year = datetime.now().year + 1

        creation_response = client.post("/v1/batch", json={
            "cnpj": company_doc,
            "ref": "something",
            "expiry_date": f"12/09/{next_year}",
            "store_unit": 1
        })

        assert creation_response.status_code == 204

        deletion_response = client.delete("/v1/batch/something")

        assert deletion_response.status_code == 204

        batch = batch_repository.get(filter={"reference": "something"}, can_raises=False)

        assert not batch

    def test_should_fail_when_unexists(self, mocker):
        with pytest.raises(MissingDoc) as error:
            client.delete("/v1/batch/something")

        assert error.value.message == "Batch not found."

    def test_should_also_delete_the_product(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)
        product_repository = ProductRepository(product_document=Product)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        next_year = datetime.now().year + 1

        creation_response = client.post("/v1/batch", json={
            "cnpj": company_doc,
            "ref": "something",
            "expiry_date": f"12/09/{next_year}",
            "store_unit": 1
        })

        assert creation_response.status_code == 204

        product_creation_resp = client.post("/v1/product", json={
            "name": "Caneta Bic",
            "price": 1.25,
            "base_stock": 125,
            "batch": "something",
            "discount_value": 1.25,
            "type": "education",
            "for_use": "for_sale",
            "bar_code": "3234567891021"
        })

        assert product_creation_resp.status_code == 204

        deletion_response = client.delete("/v1/batch/something")

        assert deletion_response.status_code == 204

        batch = batch_repository.get(filter={"reference": "something"}, can_raises=False)

        assert not batch

        product = product_repository.get(filter={"bar_code": "3234567891021"}, can_raises=False)

        assert not product

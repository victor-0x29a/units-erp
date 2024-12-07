import pytest
from datetime import datetime
from main import app
from repositories import StoreRepository
from documents import Store
from exceptions import MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.constants import company_doc
from ...__mocks__.test_client import create_test_client

client = create_test_client(app)


class TestGetBatchIntegrationV1():
    def test_should_get(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        next_year = datetime.now().year + 1

        response = client.post("/v1/batch", json={
            "cnpj": company_doc,
            "ref": "something",
            "expiry_date": f"12/09/{next_year}",
            "store_unit": 1
        })

        assert response.status_code == 204

        created_batch = client.get("/v1/batch/something").json()

        assert created_batch
        assert created_batch['reference'] == "something"
        assert created_batch['store_unit'] == 1
        assert created_batch['cnpj'] == company_doc

    def test_should_fail_when_batch_unexists(self, mocker):
        with pytest.raises(MissingDoc) as error:
            client.get("/v1/batch/something")

        assert error
        assert error.value.message == "Batch not found."

import pytest
from datetime import datetime, timedelta
from main import app
from repositories import StoreRepository, BatchRepository
from documents import Batch, Store
from exceptions import LessThanCurrentDate, UniqueKey, MissingDoc
from utils.dates import get_now, from_date_to_str
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.constants import company_doc
from ...__mocks__.test_client import create_test_client

client = create_test_client(app)


class TestCreateBatchIntegrationV1():
    def test_should_create(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)

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

        created_batch = batch_repository.get(filter={"reference": "something"})

        assert created_batch

    def test_should_reject_when_already_exists_with_same_ref(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        next_year = datetime.now().year + 1

        creation_payload = {
            "cnpj": company_doc,
            "ref": "something",
            "expiry_date": f"12/09/{next_year}",
            "store_unit": 1
        }

        client.post("/v1/batch", json=creation_payload)

        with pytest.raises(UniqueKey) as exception:
            client.post("/v1/batch", json=creation_payload)

        assert exception.value.message == "Batch already exists by reference."

    def test_should_reject_when_expiry_date_is_less_than_current_date(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        with pytest.raises(LessThanCurrentDate) as exception:
            client.post("/v1/batch", json={
                "cnpj": company_doc,
                "ref": "something",
                "expiry_date": from_date_to_str(get_now() - timedelta(days=1)),
                "store_unit": 1
            })

        assert exception.value.message == "Expiry date must be greater than current date."

    def test_should_reject_when_supplier_document_is_invalid(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        with pytest.raises(Exception) as error:
            client.post("/v1/batch", json={
                "cnpj": "123456789",
                "ref": "something",
                "expiry_date": from_date_to_str(get_now() + timedelta(days=1)),
                "store_unit": 1
            })

        assert error.value.errors.get('supplier_document').message == "The company doc should be valid."

    def test_should_reject_when_store_unexists(self, mocker):
        next_year = datetime.now().year + 1

        with pytest.raises(MissingDoc) as error:
            client.post("/v1/batch", json={
                "cnpj": company_doc,
                "ref": "something",
                "expiry_date": f"12/09/{next_year}",
                "store_unit": 1
            })

        assert error.value.message == "Store not found."

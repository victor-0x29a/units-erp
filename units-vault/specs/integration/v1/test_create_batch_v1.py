import pytest
from unittest.mock import MagicMock
from bson import ObjectId
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app
from documents import Batch, Store
from exceptions import LessThanCurrentDate, AlreadyExists, MissingDoc
from utils.dates import get_now, from_date_to_str
from ...fixture import mongo_connection # noqa: F401, E261

client = TestClient(app)


class TestCreateBatchIntegrationV1():
    def test_should_create(self, mocker):
        next_year = datetime.now().year + 1

        mocker.patch.object(Batch, 'objects', return_value=None)

        mocker.patch.object(Batch, 'save', return_value=True)

        magic_store = MagicMock()
        magic_store.id = ObjectId()

        mocker.patch.object(Store, 'objects', return_value=magic_store)

        response = client.post("/v1/batch", json={
            "cnpj": "04.954.588/0001-73",
            "ref": "something",
            "expiry_date": f"12/09/{next_year}",
            "store_unit": 1
        })

        assert response.status_code == 204

    def test_should_reject_when_already_exists_with_same_ref(self, mocker):
        next_year = datetime.now().year + 1

        mocker.patch.object(Batch, 'objects', return_value=True)

        with pytest.raises(AlreadyExists) as exception:
            client.post("/v1/batch", json={
                "cnpj": "04.954.588/0001-73",
                "ref": "something",
                "expiry_date": f"12/09/{next_year}",
                "store_unit": 1
            })

        assert exception.value.message == "Batch already exists by reference."

    def test_should_reject_when_expiry_date_is_less_than_current_date(self, mocker):
        mocker.patch.object(Batch, 'objects', return_value=False)

        with pytest.raises(LessThanCurrentDate) as exception:
            client.post("/v1/batch", json={
                "cnpj": "04.954.588/0001-73",
                "ref": "something",
                "expiry_date": from_date_to_str(get_now() - timedelta(days=1)),
                "store_unit": 1
            })

        assert exception.value.message == "Expiry date must be greater than current date."

    def test_should_reject_when_supplier_document_is_invalid(self, mocker):
        mocker.patch.object(Batch, 'objects', return_value=False)

        magic_store = MagicMock()
        magic_store.id = ObjectId()

        mocker.patch.object(Store, 'objects', return_value=magic_store)

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

        mocker.patch.object(Batch, 'objects', return_value=None)

        mocker.patch.object(Batch, 'save', return_value=True)

        magic_store = MagicMock()
        magic_store.first.return_value = None

        mocker.patch.object(Store, 'objects', return_value=magic_store)

        with pytest.raises(MissingDoc) as error:
            client.post("/v1/batch", json={
                "cnpj": "04.954.588/0001-73",
                "ref": "something",
                "expiry_date": f"12/09/{next_year}",
                "store_unit": 1
            })

        assert error.value.message == "Store not found."

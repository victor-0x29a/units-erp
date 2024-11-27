from main import app
import pytest
from documents import Store
from repositories import StoreRepository
from fastapi.testclient import TestClient
from exceptions import MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261

client = TestClient(app)


class TestGetStoreIntegrationV1():
    def test_should_get(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        creation_data = {
            "name": "Store 88",
            "unit": 88
        }

        store_repository.create(data=creation_data)

        store = client.get(f"/v1/store/{creation_data['unit']}").json()

        assert store["name"] == creation_data["name"]
        assert store["unit"] == creation_data["unit"]

    def test_should_fail_when_unexists_store(self, mocker):
        with pytest.raises(MissingDoc) as error:
            client.get("/v1/store/15")

        assert error.value.message == "Store not found."

from main import app
import pytest
from documents import Store
from repositories import StoreRepository
from fastapi.testclient import TestClient
from exceptions import MissingDoc, UniqueKey
from ...fixture import mongo_connection # noqa: F401, E261

client = TestClient(app)


class TestUpdateStoreIntegrationV1():
    def test_should_update(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_creation_data = {
            "name": "Store 88",
            "unit": 88
        }

        store_repository.create(data=store_creation_data)

        update_response = client.put(f"/v1/store/{store_creation_data['unit']}", json={
            "name": "victor-0x29a"
        })

        assert update_response.status_code == 204

        store = client.get(f"/v1/store/{store_creation_data['unit']}").json()

        assert store["name"] == "victor-0x29a"

    def test_should_fail_when_not_exists_by_unit(self, mocker):
        with pytest.raises(MissingDoc) as error:
            client.put("/v1/store/1", json={
                "name": "victor-0x29a"
            })

        assert error.value.message == 'Store not found.'

    def test_should_fail_when_already_exists_by_unit(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "name": "Store 88",
            "unit": 9
        })

        store_repository.create(data={
            "name": "Store 88",
            "unit": 10
        })

        with pytest.raises(UniqueKey) as error:
            client.put("/v1/store/10", json={
                "unit": 9
            })

        assert error.value.message == 'Already exist a store with the same unit.'

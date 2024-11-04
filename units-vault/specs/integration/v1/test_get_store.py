from main import app
import pytest
from documents import Store
from unittest.mock import MagicMock
from bson import ObjectId
from fastapi.testclient import TestClient
from exceptions import MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261

client = TestClient(app)


class TestGetStoreIntegrationV1():
    def test_should_get(self, mocker):
        creation_data = {
            "id": str(ObjectId()),
            "name": "Store 88",
            "unit": 88,
            "latitude": 0.0,
            "longitude": 0.0
        }

        magic_objects = MagicMock()

        magic_objects.first.return_value = creation_data

        mocker.patch.object(Store, 'objects', return_value=magic_objects)

        store = client.get(f"/v1/store/{creation_data['unit']}").json()

        assert store["name"] == creation_data["name"]
        assert store["unit"] == creation_data["unit"]
        assert store["id"] == creation_data["id"]

    def test_should_fail_when_unexists_store(self, mocker):
        creation_data = {
            "id": str(ObjectId()),
            "name": "Store 88",
            "unit": 88,
            "latitude": 0.0,
            "longitude": 0.0
        }

        magic_objects = MagicMock()

        magic_objects.first.return_value = None

        mocker.patch.object(Store, 'objects', return_value=magic_objects)

        with pytest.raises(MissingDoc) as error:
            client.get(f"/v1/store/{creation_data['unit']}")

        assert error.value.message == "Store not found."

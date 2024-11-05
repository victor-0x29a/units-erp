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
            "unit": 88
        }

        magic_object = MagicMock()

        magic_object._data = creation_data

        magic_objects = MagicMock()

        magic_objects.first.return_value = magic_object

        mocker.patch.object(Store, 'objects', return_value=magic_objects)

        store = client.get(f"/v1/store/{creation_data['unit']}").json()

        assert store["name"] == creation_data["name"]
        assert store["unit"] == creation_data["unit"]

    def test_should_fail_when_unexists_store(self, mocker):
        magic_objects = MagicMock()

        magic_objects.first.return_value = None

        mocker.patch.object(Store, 'objects', return_value=magic_objects)

        with pytest.raises(MissingDoc) as error:
            client.get("/v1/store/15")

        assert error.value.message == "Store not found."

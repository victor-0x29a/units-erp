from main import app
import pytest
from exceptions import MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.test_client import create_test_client

client = create_test_client(app)


class TestDeleteStoreIntegrationV1():
    def test_should_delete(self, mocker):
        data_creation = {
            'name': '0x store',
            'unit': 1
        }

        client.post("/v1/store", json=data_creation)

        response = client.delete(f"/v1/store/{data_creation['unit']}")

        assert response.status_code == 204

    def test_should_fail_when_unexists(self, mocker):
        with pytest.raises(MissingDoc) as error:
            client.delete("/v1/store/1")

        assert error.value.message == "Store not found."

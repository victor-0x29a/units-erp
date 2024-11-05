from main import app
import pytest
from fastapi.testclient import TestClient
from documents import Store
from exceptions import UniqueKey

client = TestClient(app)


class TestCreateStoreIntegrationV1():
    def test_should_create(self, mocker):
        mocker.patch.object(Store, 'save', return_value=True)

        mocker.patch.object(Store, 'reload', return_value=True)

        response = client.post("/v1/store", json={
            "name": "Foo",
            "unit": 1
        })

        assert response.status_code == 204

    def test_should_fail_when_already_exists_with_same_unit(self, mocker):
        client.post("/v1/store", json={
            "name": "Foo",
            "unit": 1
        })

        with pytest.raises(UniqueKey) as exception:
            client.post("/v1/store", json={
                "name": "Foo",
                "unit": 1
            })

        assert exception.value.message == "Store with same unit already exists."

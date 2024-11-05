from main import app
import pytest
from documents import Store
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from exceptions import MissingDoc, UniqueKey
from ...fixture import mongo_connection # noqa: F401, E261

client = TestClient(app)


class TestUpdateStoreIntegrationV1():
    def test_should_update(self, mocker):
        magic_objects = MagicMock()

        magic_first = MagicMock()

        magic_objects.first.return_value = magic_first

        mocker.patch.object(
            Store,
            'objects',
            return_value=magic_objects
        )

        for method in ['save', 'reload']:
            mocker.patch.object(
                Store,
                method,
                return_value=None
            )

        update_response = client.put("/v1/store/777", json={
            "name": "victor-0x29a"
        })

        assert update_response.status_code == 204

    def test_should_fail_when_not_exists_by_unit(self, mocker):
        magic_first = MagicMock()

        magic_first.first.return_value = None

        mocker.patch.object(
            Store,
            'objects',
            return_value=magic_first
        )

        with pytest.raises(MissingDoc) as error:
            client.put("/v1/store/1", json={
                "name": "victor-0x29a"
            })

        assert error.value.message == 'Store not found.'

    def test_should_fail_when_already_exists_by_unit(self, mocker):
        magic_store = MagicMock()

        magic_store.update.side_effect = UniqueKey('Already exist a store with the same unit.')

        magic_first = MagicMock()

        magic_first.first.return_value = magic_store

        mocker.patch.object(
            Store,
            'objects',
            return_value=magic_first
        )

        with pytest.raises(UniqueKey) as error:
            client.put("/v1/store/15", json={
                "name": "victor-0x29a"
            })

        assert error.value.message == 'Already exist a store with the same unit.'

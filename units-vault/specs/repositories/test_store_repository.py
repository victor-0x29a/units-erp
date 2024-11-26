import pytest
from documents import Store
from repositories import StoreRepository
from exceptions import UniqueKey, MissingParam, MissingDoc
from ..fixture import mongo_connection # noqa: F401, E261


class TestCreate:
    def test_should_create_store(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        data = {
            "unit": 1,
            "name": "Store 1"
        }

        result = store_repository.create(data)

        assert result.name == data['name']
        assert result.unit == data['unit']

    def test_should_raise_unique_key_exception(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        data = {
            "unit": 1,
            "name": "Store 1"
        }

        store_repository.create(data)

        with pytest.raises(UniqueKey) as error:
            store_repository.create(data)

        assert error.value.message == 'Store with same unit already exists.'


class TestGet:
    def test_should_get_store(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        data = {
            "unit": 1,
            "name": "Store 1"
        }

        store_repository.create(data)

        get_result = store_repository.get({'unit': 1})

        assert get_result.name == data['name']
        assert get_result.unit == data['unit']

    def test_should_fail_when_havent_filter(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        with pytest.raises(MissingParam) as error:
            store_repository.get()

        assert error.value.message == 'Filter is required.'

    def test_should_fail_when_not_found(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        with pytest.raises(MissingDoc) as error:
            store_repository.get({'unit': 1})

        assert error.value.message == 'Store not found.'


class TestUpdate:
    def test_should_update(self, mocker):
        store_creation_data = {
            "unit": 1,
            "name": "Store 1"
        }

        store_repository = StoreRepository(store_document=Store)

        store_repository.create(store_creation_data)

        update_data = {
            "name": "Store 2"
        }

        store = store_repository.get({'unit': 1})

        store_repository.update(store, update_data)

        store = store_repository.get({'unit': 1})

        assert store.name != store_creation_data['name']
        assert store.name == update_data['name']

    def test_should_fail_when_already_exists_by_unit(self, mocker):
        store_creation_data = {
            "unit": 1,
            "name": "Store 1"
        }

        store_repository = StoreRepository(store_document=Store)

        store_repository.create(store_creation_data)

        store_creation_data = {
            "unit": 2,
            "name": "Store 2"
        }

        store_repository.create(store_creation_data)

        store = store_repository.get({'unit': 1})

        update_data = {
            "unit": 2
        }

        with pytest.raises(UniqueKey) as error:
            store_repository.update(store, update_data)

        assert error.value.message == 'Store with same unit already exists.'

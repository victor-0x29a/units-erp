import pytest
from services.v1.store_service import StoreService as StoreServiceV1
from exceptions import InternalError, UniqueKey, MissingParam, MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261


class TestCreateV1:
    def test_should_create_store(self, mocker):
        data = {
            'name': '0x store',
            'unit': 1
        }

        service = StoreServiceV1()

        service.instance(data=data)

        res = service.create()

        for keys in data.keys():
            assert getattr(res, keys) == data[keys]

    def test_should_fail_when_havent_instance(self, mocker):
        service = StoreServiceV1()

        with pytest.raises(InternalError) as error:
            service.create()

        assert error.value.message == 'Store instance are not initialized.'

    def test_should_fail_when_already_exists_by_unit(self, mocker):
        data = {
            'name': '0x store',
            'unit': 1
        }

        service = StoreServiceV1()

        service.instance(data=data)

        service.create()

        service.instance(data=data)

        with pytest.raises(UniqueKey) as error:
            service.create()

        assert error.value.message == 'Store with same unit already exists.'


class TestDeleteV1:
    def test_should_delete(self, mocker):
        data = {
            'name': '0x store',
            'unit': 1
        }

        service = StoreServiceV1()

        service.instance(data=data)

        service.create()

        delete_return = service.delete(unit=1)

        assert not delete_return

    def test_should_fail_when_not_exists_by_unit(self, mocker):
        service = StoreServiceV1()

        with pytest.raises(MissingDoc) as error:
            service.delete(unit=1)

        assert error.value.message == 'Store not found.'


class TestGetV1:
    def test_should_get(self, mocker):
        creation_data = {
            'name': 'Store 65',
            'unit': 65
        }

        service = StoreServiceV1()

        service.instance(data=creation_data)

        service.create()

        filter_data = {
            'unit': 65
        }

        store = service.get(filter=filter_data)

        assert store.name == creation_data['name']
        assert store.unit == creation_data['unit']
        assert not bool(store.latitude)
        assert not bool(store.longitude)

    def test_should_fail_when_havent_filter(self, mocker):
        service = StoreServiceV1()

        with pytest.raises(MissingParam) as error:
            service.get(filter={})

        assert error.value.message == 'Filter is required.'

    def test_should_fail_when_unexists_store(self, mocker):
        service = StoreServiceV1()

        with pytest.raises(MissingDoc) as error:
            service.get(filter={"unit": 999})

        assert error

import pytest
from services.v1.store_service import StoreService as StoreServiceV1
from exceptions import InternalError, UniqueKey
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

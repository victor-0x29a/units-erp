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


class TestUpdateV1:
    def test_should_update(self, mocker):
        creation_data = {
            'name': 'Store 65',
            'unit': 65
        }

        service = StoreServiceV1()

        service.instance(data=creation_data)

        service.create()

        update_data = {
            'name': '0x'
        }

        updated_store = service.update(creation_data['unit'], update_data)

        assert updated_store['name'] == update_data['name']

    def test_should_fail_when_unexists(self, mocker):
        service = StoreServiceV1()

        update_data = {
            'name': '0x'
        }

        with pytest.raises(MissingDoc) as error:
            service.update(unit=999, data_for_update=update_data)

        assert error.value.message == 'Store not found.'

    def test_should_fail_when_already_exists_by_unit(self, mocker):
        creation_datas = [
            {
                'name': 'Store 65',
                'unit': 65
            },
            {
                'name': 'Store 66',
                'unit': 66
            }
        ]

        service = StoreServiceV1()

        service.instance(data=creation_datas[0])

        service.create()

        service.instance(data=creation_datas[1])

        service.create()

        update_data = {
            'unit': 65
        }

        with pytest.raises(UniqueKey) as error:
            service.update(
                unit=creation_datas[1]['unit'],
                data_for_update=update_data
            )

        assert error

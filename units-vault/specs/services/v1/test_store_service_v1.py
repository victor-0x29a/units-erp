import pytest
from datetime import timedelta
from documents import Batch, Product, Employee, Store
from repositories import BatchRepository, ProductRepository, EmployeeRepository, StoreRepository
from services.v1.store_service import StoreService as StoreServiceV1
from exceptions import InternalError, UniqueKey, MissingParam, MissingDoc
from ...fixture import mongo_connection # noqa: F401, E261
from utils.dates import get_now
from ...__mocks__.constants import company_doc, human_doc, human_doc_2


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

    def test_should_delete_all_childrens(self, mocker):
        batch_repository = BatchRepository(Batch)
        product_repository = ProductRepository(Product)
        employee_repository = EmployeeRepository(Employee)
        store_repository = StoreRepository(Store)

        store_data = {
            'name': '0x store',
            'unit': 1
        }

        service = StoreServiceV1()

        store = store_repository.create(data=store_data)

        batches_data = [
            {
                "expiry_date": get_now() + timedelta(days=1),
                "inserction_datetime": get_now(),
                "supplier_document": company_doc,
                "reference": "REFERER001",
                "store": store.pk
            },
            {
                "expiry_date": get_now() + timedelta(days=1),
                "inserction_datetime": get_now(),
                "supplier_document": company_doc,
                "reference": "REFERER002",
                "store": store.pk
            }
        ]

        employees_data = [
            {
                "document": human_doc,
                "name": "Foo",
                "username": "foo",
                "role": "ADMIN",
                "store_unit": store.pk
            },
            {
                "document": human_doc_2,
                "name": "Bar",
                "username": "bar",
                "role": "ADMIN",
                "store_unit": store.pk
            }
        ]

        products_data = [
            {
                'batch': None,
                'price': 10,
                'discount_value': 1,
                'bar_code': '1234567891012',
                'name': 'foo name',
                'stock': 5,
                'item_type': 'foo type'
            },
            {
                'batch': None,
                'price': 10,
                'discount_value': 1,
                'bar_code': '1334567891012',
                'name': 'foo name',
                'stock': 5,
                'item_type': 'foo type'
            }
        ]

        for i, batch_data in enumerate(batches_data):
            batch = batch_repository.create(data=batch_data)

            products_data[i]['batch'] = batch.pk

            assert batch

        for employee_data in employees_data:
            employee = employee_repository.create(data=employee_data)
            assert employee

        for product_data in products_data:
            product = product_repository.create(data=product_data)
            assert product

        service.delete(unit=1)

        with pytest.raises(MissingDoc) as error:
            store_repository.get(filter={'unit': 1})

        assert error
        assert error.value.message == 'Store not found.'

        batches = batch_repository.get(filters={'store': store.pk}, is_only_one=False)

        assert not bool(batches)

        for product_data in products_data:
            with pytest.raises(MissingDoc) as error:
                product_repository.get(filters={'bar_code': product_data['bar_code']})

            assert error
            assert error.value.message == 'Product not found.'

        for employee_data in employees_data:
            with pytest.raises(MissingDoc) as error:
                employee_repository.get(filter={'document': employee_data['document']})

            assert error
            assert error.value.message == 'Employee not found.'


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

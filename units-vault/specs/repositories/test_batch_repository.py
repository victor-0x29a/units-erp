import pytest
from datetime import timedelta
from documents import Store, Batch
from use_cases import CreateBatchV1
from utils.dates import get_now
from repositories import StoreRepository, BatchRepository
from exceptions import MissingParam, MissingDoc, UniqueKey
from ..fixture import mongo_connection # noqa: F401, E261


class TestCreate:
    def test_should_create(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)
        store_repository = StoreRepository(store_document=Store)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch = batch_repository.create(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": "10.076.086/0001-90",
            "reference": "REFERER001",
            "store": store.pk
        })

        assert batch
        assert batch.reference == 'REFERER001'

    def test_should_fail_when_has_already_exists_by_ref(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)
        store_repository = StoreRepository(store_document=Store)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch_repository.create(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": "10.076.086/0001-90",
            "reference": "REFERER001",
            "store": store.pk
        })

        with pytest.raises(UniqueKey) as error:
            batch_repository.create(data={
                "expiry_date": get_now() + timedelta(days=1),
                "inserction_datetime": get_now(),
                "supplier_document": "10.076.086/0001-90",
                "reference": "REFERER001",
                "store": store.pk
            })

        assert error.value.message == 'Batch already exists by reference.'


class TestGet:
    def test_should_get(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch = CreateBatchV1(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": "10.076.086/0001-90",
            "reference": "REFERER001",
            "store_unit": 1
        }).start()

        assert batch

        batch = batch_repository.get(filters={'reference': 'REFERER001'}, can_raises=False)

        assert batch
        assert batch.reference == 'REFERER001'

    def test_should_fails_when_unexists_batch(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)

        with pytest.raises(MissingDoc) as error:
            batch_repository.get(filters={
                'reference': 'REFERER001'
            })

        assert error.value.message == 'Batch not found.'

    def test_should_not_fails_when_unexists_batch_and_cant_raises(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)

        batch = batch_repository.get(filters={
            'reference': 'REFERER001'
        }, can_raises=False)

        assert not batch

    def test_should_fails_when_havent_filters(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)

        with pytest.raises(MissingParam) as error:
            batch_repository.get(filters=None)

        assert error.value.message == 'Filter is required.'


class TestDelete:
    def test_should_delete(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch = CreateBatchV1(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": "10.076.086/0001-90",
            "reference": "REFERER001",
            "store_unit": 1
        }).start()

        assert batch

        batch_repository.delete(batch=batch)

        batch = batch_repository.get(filters={'reference': 'REFERER001'}, can_raises=False)

        assert not batch

    def test_should_fail_when_havent_batch(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)

        with pytest.raises(MissingParam) as error:
            batch_repository.delete(batch=None)

        assert error.value.message == 'Batch is required.'

import datetime
import pytest
from unittest.mock import MagicMock
from bson import ObjectId
from use_cases import CreateBatchV1
from documents import Batch, Store
from utils.dates import get_now
from exceptions import MissingParam, MissingDoc
from ..fixture import mongo_connection # noqa: F401, E261


class TestCreateBatchUseCaseV1:
    def test_create_batch(self, mocker):
        magic_store = MagicMock()
        magic_store.id = ObjectId()

        mocker.patch.object(Store, 'objects', return_value=magic_store)

        data = {
            'expiry_date': get_now() + datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "29662565000116",
            'reference': "123123",
            "store_unit": 1
        }

        mocker.patch.object(Batch, 'objects', return_value=None)

        mocker.patch.object(Batch, 'save', return_value=True)

        batch = CreateBatchV1(
            data=data
        ).start()

        assert batch

    def test_should_fail_when_exists_batch_with_same_ref(self, mocker):
        data = {
            'expiry_date': get_now() + datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "29662565000116",
            'reference': "123123"
        }

        mocker.patch.object(Batch, 'objects', return_value=True)

        with pytest.raises(Exception) as error:
            CreateBatchV1(
                data=data
            ).start()

        assert 'Batch already exists by reference.' in str(error)

    def test_should_fail_when_expiry_date_less_than_current_date(self, mocker):
        data = {
            'expiry_date': get_now() - datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "29662565000116",
            'reference': "123123"
        }

        mocker.patch.object(Batch, 'objects', return_value=None)

        with pytest.raises(Exception) as error:
            CreateBatchV1(
                data=data
            ).start()

        assert 'LessThanCurrentDate' in str(error)

    def test_should_fail_when_supplier_document_is_invalid(self, mocker):
        magic_store = MagicMock()
        magic_store.id = ObjectId()

        mocker.patch.object(Store, 'objects', return_value=magic_store)

        data = {
            'expiry_date': get_now() + datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "923148328",
            'reference': "123123",
            'store_unit': 1
        }

        mocker.patch.object(Batch, 'objects', return_value=None)

        with pytest.raises(Exception) as error:
            CreateBatchV1(
                data=data
            ).start()

        assert error.value.errors.get('supplier_document').message == 'The company doc should be valid.'

    def test_should_fail_when_havent_store(self, mocker):
        data = {
            'expiry_date': get_now() + datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "29662565000116",
            'reference': "123123"
        }

        mocker.patch.object(Batch, 'objects', return_value=None)

        mocker.patch.object(Store, 'objects', return_value=None)

        with pytest.raises(MissingParam) as error:
            CreateBatchV1(
                data=data
            ).start()

        assert error.value.message == 'Store is required for create a batch.'

    def test_should_fail_when_unexists_store(self, mocker):
        data = {
            'expiry_date': get_now() + datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "29662565000116",
            'reference': "123123",
            'store_unit': 1
        }

        mocker.patch.object(Batch, 'objects', return_value=None)

        magic_objects = MagicMock()

        magic_objects.first.return_value = None

        mocker.patch.object(Store, 'objects', return_value=magic_objects)

        with pytest.raises(MissingDoc) as error:
            CreateBatchV1(
                data=data
            ).start()

        assert error.value.message == 'Store not found.'

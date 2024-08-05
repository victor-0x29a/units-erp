import datetime
import pytest
from use_cases import CreateBatchV1
from documents import Batch
from utils.dates import get_now
from ..fixture import mongo_connection # noqa: F401, E261


class TestCreateBatchUseCaseV1:
    def test_create_batch(self, mocker):
        data = {
            'expiry_date': get_now() + datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "29662565000116",
            'reference': "123123"
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
        data = {
            'expiry_date': get_now() + datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "923148328",
            'reference': "123123"
        }

        mocker.patch.object(Batch, 'objects', return_value=None)

        with pytest.raises(Exception) as error:
            CreateBatchV1(
                data=data
            ).start()

        assert 'The company doc should be valid.' == error.value.errors.get('supplier_document').message

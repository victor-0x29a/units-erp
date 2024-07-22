import datetime
import pytest
from use_cases import CreateBatchV1
from utils.dates import get_now


class TestCreateBatchUseCaseV1:
    def test_create_batch(self, mocker):
        data = {
            'expiry_date': get_now() + datetime.timedelta(days=1),
            'inserction_datetime': get_now(),
            'supplier_document': "29662565000116",
            'reference': "123123"
        }

        mock_batch = mocker.patch('documents.Batch')

        mocker.patch.object(mock_batch, 'objects', return_value=None)

        mocker.patch.object(mock_batch, 'save', return_value=True)

        batch = CreateBatchV1(
            batch_document=mock_batch,
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

        mock_batch = mocker.patch('documents.Batch')

        mocker.patch.object(mock_batch, 'objects', return_value=True)

        with pytest.raises(Exception) as error:
            CreateBatchV1(
                batch_document=mock_batch,
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

        mock_batch = mocker.patch('documents.Batch')

        mocker.patch.object(mock_batch, 'objects', return_value=None)

        with pytest.raises(Exception) as error:
            CreateBatchV1(
                batch_document=mock_batch,
                data=data
            ).start()

        assert 'LessThanCurrentDate' in str(error)

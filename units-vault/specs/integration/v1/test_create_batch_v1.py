from main import app
import pytest
from fastapi.testclient import TestClient
from documents import Batch
from exceptions import LessThanCurrentDate, AlreadyExists
from datetime import datetime
from utils.dates import get_now

client = TestClient(app)


class TestCreateBatchIntegrationV1():
    def test_should_create(self, mocker):
        next_year = datetime.now().year + 1

        mocker.patch.object(Batch, 'objects', return_value=None)

        mocker.patch.object(Batch, 'save', return_value=True)

        response = client.post("/v1/batch", json={
            "cnpj": "any",
            "ref": "something",
            "expiry_date": f"12/09/{next_year}"
        })

        assert response.status_code == 204

    def test_should_reject_when_already_exists_with_same_ref(self, mocker):
        next_year = datetime.now().year + 1

        mocker.patch.object(Batch, 'objects', return_value=True)

        with pytest.raises(AlreadyExists) as exception:
            client.post("/v1/batch", json={
                "cnpj": "any",
                "ref": "something",
                "expiry_date": f"12/09/{next_year}"
            })

        assert exception.value.message == "Batch already exists by reference."

    def test_should_reject_when_expiry_date_is_less_than_current_date(self, mocker):
        now = get_now()
        current_year = now.year
        current_month = now.month
        last_day = now.day - 1

        mocker.patch.object(Batch, 'objects', return_value=False)

        with pytest.raises(LessThanCurrentDate) as exception:
            client.post("/v1/batch", json={
                "cnpj": "any",
                "ref": "something",
                "expiry_date": f"{last_day}/{current_month}/{current_year}"
            })

        assert exception.value.message == "Expiry date must be greater than current date."
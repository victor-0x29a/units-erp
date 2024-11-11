import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from documents import Employee
from exceptions import MissingDoc
from ...__mocks__.constants import human_doc
from ...fixture import mongo_connection # noqa: F401, E261

client = TestClient(app)


class TestDeleteEmployeeIntegrationV1():
    def test_should_delete(self, mocker):
        magic_first = MagicMock()

        magic_first.delete.return_value = True

        magic_employee = MagicMock()

        magic_employee.first = magic_first

        mocker.patch.object(
            Employee,
            'objects',
            return_value=magic_employee
        )

        response = client.delete(f"/v1/employee/{human_doc}")

        assert response.status_code == 204

    def test_should_fail_when_employee_unexists(self, mocker):
        magic_employee = MagicMock()

        magic_employee.first.return_value = None

        mocker.patch.object(
            Employee,
            'objects',
            return_value=magic_employee
        )

        with pytest.raises(MissingDoc) as error:
            client.delete(f"/v1/employee/{human_doc}")

        assert error.value.message == 'Employee not found.'

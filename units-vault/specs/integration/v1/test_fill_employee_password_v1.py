from main import app
import pytest
from documents import Employee
from unittest.mock import MagicMock
from ...__mocks__.test_client import create_test_client
from exceptions import MissingDoc, InvalidParam
from ...fixture import mongo_connection # noqa: F401, E261

client = create_test_client(app)


class TestFillEmployeePasswdIntegrationV1():
    def test_should_fill(self, mocker):
        update_data = {
            "password": "strongpassword"
        }

        magic_employee = MagicMock()

        magic_first = MagicMock()

        magic_first.password = None

        magic_first.save.return_value = True

        magic_employee.first.return_value = magic_first

        mocker.patch.object(
            Employee,
            'objects',
            return_value=magic_employee
        )

        response = client.put('/v1/employee/19391239/password', json=update_data)

        assert response.status_code == 204

    def test_should_fail_when_already_is_filled(self, mocker):
        update_data = {
            "password": "strongpassword"
        }

        magic_employee = MagicMock()

        magic_first = MagicMock()

        magic_first.password = 'strongpassword'

        magic_employee.first.return_value = magic_first

        mocker.patch.object(
            Employee,
            'objects',
            return_value=magic_employee
        )

        with pytest.raises(InvalidParam) as error:
            client.put('/v1/employee/19391239/password', json=update_data)

        assert error.value.message == 'Failed on process.'

    def test_should_fail_when_unexistent_employee(self, mocker):
        update_data = {
            "password": "strongpassword"
        }

        mocker.patch.object(
            Employee,
            'objects',
            side_effect=MissingDoc('Employee not found.')
        )

        with pytest.raises(MissingDoc) as error:
            client.put('/v1/employee/19391239/password', json=update_data)

        assert error.value.message == 'Employee not found.'

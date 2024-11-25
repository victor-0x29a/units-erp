import pytest
from documents import Store
from repositories import EmployeeRepository, StoreRepository
from exceptions import InvalidParam, UniqueKey, MissingDoc, MissingParam
from ..fixture import mongo_connection # noqa: F401, E261
from ..__mocks__.constants import human_doc, human_doc_2


class TestCreate:
    def test_should_create_an_employee(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "foo",
            "role": "ADMIN",
            "store_unit": store.pk
        }

        employee = employee_repository.create(data=employee_creation_data)

        assert employee
        assert employee.name == employee_creation_data['name']

    def test_should_create_an_employee_with_pwd(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "foo",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": "password"
        }

        employee = employee_repository.create(data=employee_creation_data)

        assert employee
        assert employee.name == employee_creation_data['name']
        assert employee.password
        assert isinstance(employee.password, str)
        assert employee.password != employee_creation_data['password']

    def test_should_fail_create_with_an_invalid_role(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "foo",
            "role": "ADMIN2",
            "store_unit": store.pk,
            "password": "password"
        }

        with pytest.raises(InvalidParam) as error:
            employee_repository.create(data=employee_creation_data)

        assert error
        assert error.value.message == "The role is invalid, valid roles are: ADMIN, FINANCIAL, INVENTOR, OPERATOR" # noqa

    def test_should_fail_when_already_exists_by_document(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "foo",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": "password"
        }

        employee_repository.create(data=employee_creation_data)

        with pytest.raises(UniqueKey) as error:
            employee_creation_data["username"] = "foo2"
            employee_repository.create(data=employee_creation_data)

        assert error
        assert error.value.message == "The document has already been taken."

    def test_should_fail_when_already_exists_by_username(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "foo",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": "password"
        }

        employee_repository.create(data=employee_creation_data)

        with pytest.raises(UniqueKey) as error:
            employee_creation_data["document"] = human_doc_2
            employee_repository.create(data=employee_creation_data)

        assert error
        assert error.value.message == "The username has already been taken."


class TestGet:
    def test_should_get_an_employee(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo"
        }

        store = store_repository.create(store_creation_data)

        data = {
            "name": "Employee 1",
            "document": human_doc,
            "store_unit": store.id,
            "username": "employee1",
            "role": "ADMIN"
        }

        employee = employee_repository.create(data)

        employee = employee_repository.get({'document': human_doc})

        assert employee
        assert employee.name == data['name']
        assert employee.document == data['document']
        assert employee.role == data['role']

    def test_should_not_fail_when_unexists_and_cant_raises(self, mocker):
        employee_repository = EmployeeRepository()

        employee = employee_repository.get({'document': human_doc}, can_raises=False)

        assert not employee

    def test_should_fail_when_unexists_and_can_raises(self, mocker):
        employee_repository = EmployeeRepository()

        with pytest.raises(MissingDoc) as error:
            employee_repository.get({'document': human_doc})

        assert error
        assert error.value.message == "Employee not found."

    def test_should_fail_when_havent_filters(self, mocker):
        employee_repository = EmployeeRepository()

        with pytest.raises(MissingParam) as error:
            employee_repository.get({})

        assert error
        assert error.value.message == "Filter is required."


class TestFillPassword:
    def test_should_fill_password(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo"
        }

        store = store_repository.create(store_creation_data)

        data = {
            "name": "Employee 1",
            "document": human_doc,
            "store_unit": store.id,
            "username": "employee1",
            "role": "ADMIN"
        }

        employee = employee_repository.create(data)

        assert not employee.password

        employee_repository.fill_password(employee=employee, password="password")

        employee = employee_repository.get(filter={'document': human_doc})

        assert employee
        assert employee.password
        assert isinstance(employee.password, str)

    def test_should_fail_when_already_have_password(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo"
        }

        store = store_repository.create(store_creation_data)

        data = {
            "name": "Employee 1",
            "document": human_doc,
            "store_unit": store.id,
            "username": "employee1",
            "role": "ADMIN",
            "password": "password"
        }

        employee = employee_repository.create(data)

        with pytest.raises(InvalidParam) as error:
            employee_repository.fill_password(employee=employee, password="password")

        assert error
        assert error.value.message == "Failed on process."

    def test_should_fail_when_havent_employee(self, mocker):
        employee_repository = EmployeeRepository()
        with pytest.raises(MissingParam) as error:
            employee_repository.fill_password(employee=None, password="password")

        assert error
        assert error.value.message == "Employee is required."


class TestDelete:
    def test_should_delete_an_employee(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository()

        store_creation_data = {
            "unit": 1,
            "name": "Foo"
        }

        store = store_repository.create(store_creation_data)

        data = {
            "name": "Employee 1",
            "document": human_doc,
            "store_unit": store.id,
            "username": "employee1",
            "role": "ADMIN"
        }

        employee = employee_repository.create(data)

        assert employee

        employee_repository.delete(employee=employee)

        employee = employee_repository.get(filter={'document': human_doc}, can_raises=False)

        assert not employee

    def test_should_fail_when_havent_employee(self, mocker):
        employee_repository = EmployeeRepository()
        with pytest.raises(MissingParam) as error:
            employee_repository.delete(employee=None)

        assert error
        assert error.value.message == "Employee is required."

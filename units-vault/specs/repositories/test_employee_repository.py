from repositories import EmployeeRepository, StoreRepository
from ..fixture import mongo_connection # noqa: F401, E261
from ..__mocks__.constants import human_doc


class TestCreate:
    def test_should_create_an_employee(self, mocker):
        store_repository = StoreRepository()

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

# class TestGet:
#     def test_should_get_an_employee(self, mocker):
#         store_repository = StoreRepository()
#         employee_repository = EmployeeRepository()

#         store_creation_data = {
#             "unit": 1,
#             "name": "Foo"
#         }

#         store = store_repository.create(store_creation_data)

#         data = {
#             "name": "Employee 1",
#             "document": "12345678900",
#             "store_unit": store.id,
#             "username": "employee1",
#             "role": "ADMIN"
#         }

#         employee = employee_repository.create(data)

#         employee = employee_repository.get({'document': '12345678900'})

#         assert employee.name == data['name']
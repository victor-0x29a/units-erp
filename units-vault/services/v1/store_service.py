from repositories import StoreRepository, BatchRepository, ProductRepository, EmployeeRepository
from documents import Store, Batch, Product, Employee
from mongoengine.errors import NotUniqueError
from exceptions import InternalError, UniqueKey, MissingParam, MissingDoc


class StoreService:
    def __init__(self):
        self.__instance = None
        self.repository = StoreRepository(store_document=Store)
        self.batch_repository = BatchRepository(batch_document=Batch)
        self.product_repository = ProductRepository(product_document=Product)
        self.employee_repository = EmployeeRepository(employee_document=Employee)

    def create(self):
        self.__validate_creation()

        self.__instance = Store(**self.__instance)

        try:
            self.__instance.save()

            self.__instance.reload()

            return self.__instance
        except NotUniqueError:
            raise UniqueKey('Store with same unit already exists.')

    def instance(self, data={}):
        self.__instance = data

    def __validate_creation(self):
        if not self.__instance:
            raise InternalError('Store instance are not initialized.')

    def delete(self, unit: int):
        store = self.repository.get(filter={'unit': unit})

        batches = self.batch_repository.get(
            filter={'store': store.pk},
            can_raises=False,
            is_only_one=False
        )

        employees = self.employee_repository.get(
            filter={'store_unit': store.pk},
            can_raises=False,
            is_only_one=False
        )

        for batch in batches:
            product = self.product_repository.get(
                filter={'batch': batch.pk},
                can_raises=False
            )

            self.product_repository.delete(product=product)

            self.batch_repository.delete(batch=batch)

        for employee in employees:
            self.employee_repository.delete(employee=employee)

        store.delete()

    def get(self, filter={}):
        has_filter = bool(len(filter.keys()))

        if not has_filter:
            raise MissingParam("Filter is required.")

        store = Store.objects(**filter).first()

        if not store:
            raise MissingDoc("Store not found.")

        return store

    def update(self, unit: int, data_for_update: dict):
        store = self.get({'unit': unit})

        update_fields = data_for_update.keys()
        current_data = store._data

        for field in update_fields:
            data = data_for_update[field]
            if data:
                current_data[field] = data

        try:
            store.update(**current_data)
        except NotUniqueError:
            raise UniqueKey("Already exist a store with the same unit.")

        store.reload()

        store.save()

        return store._data

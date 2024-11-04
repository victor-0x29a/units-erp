from documents import Store
from mongoengine.errors import NotUniqueError
from exceptions import InternalError, UniqueKey, MissingParam, MissingDoc


class StoreService:
    def __init__(self):
        self.__instance = None

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
        try:
            store = Store.objects.get(unit=unit)
            return store.delete()
        except Store.DoesNotExist:
            raise MissingDoc('Store not found.')

    def get(self, filter={}):
        has_filter = bool(len(filter.keys()))

        if not has_filter:
            raise MissingParam("Filter is required.")

        store = Store.objects(**filter).first()

        if not store or not bool(len(store)):
            raise MissingDoc("Store not found.")

        return store

from documents import Store
from mongoengine.errors import NotUniqueError
from exceptions import InternalError, UniqueKey


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

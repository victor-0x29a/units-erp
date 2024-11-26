from documents import Store
from mongoengine.errors import NotUniqueError
from exceptions import UniqueKey, MissingParam, MissingDoc


class StoreRepository:
    def __init__(self, store_document: Store):
        self.Store = store_document

    def create(self, data) -> Store:
        store = self.Store(**data)

        try:
            store.save()

            store.reload()

            return store
        except NotUniqueError:
            raise UniqueKey('Store with same unit already exists.')

    def get(self, filter=None) -> Store:
        if not filter:
            raise MissingParam("Filter is required.")

        store = self.Store.objects(**filter).first()

        if not store:
            raise MissingDoc("Store not found.")

        return store

    def update(self, store: Store, new_data: dict) -> Store:
        try:
            store.update(**new_data)
            store.reload()
        except NotUniqueError:
            raise UniqueKey('Store with same unit already exists.')

        return store

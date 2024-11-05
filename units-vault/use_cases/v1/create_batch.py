from documents import Batch
from services.v1.store_service import StoreService
from exceptions import AlreadyExists, LessThanCurrentDate, MissingParam
from utils.dates import get_now


class CreateBatch:
    def __init__(self, data={}):
        self.batch = data

        self.__validate()

        self.__fetch_store()

        self.batch_obj = Batch(**self.batch)

        self.batch_obj.validate()

    def __validate(self):
        batch = Batch.objects(reference=self.batch.get('reference', None))

        if batch:
            raise AlreadyExists(message="Batch already exists by reference.")

        current_date = get_now()

        expiry_date = self.batch.get('expiry_date', None)

        if expiry_date < current_date:
            raise LessThanCurrentDate()

        if not self.batch.get("store_unit", None):
            raise MissingParam(message="Store is required for create a batch.")

    def __fetch_store(self):
        store_service = StoreService()

        store = store_service.get({'unit': self.batch.get("store_unit")})

        del self.batch["store_unit"]

        self.batch["store"] = store.id

    def start(self) -> Batch:
        self.batch_obj.save()

        return self.batch_obj

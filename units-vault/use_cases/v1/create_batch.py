from documents import Batch
from exceptions import AlreadyExists, LessThanCurrentDate
from utils.dates import get_now


class CreateBatch:
    def __init__(self, data={}):
        self.batch = data

        self.batch_obj = Batch(**self.batch)

        self.batch_obj.validate()

        self.__validate()

    def __validate(self):
        batch = Batch.objects(reference=self.batch.get('reference', None))

        if batch:
            raise AlreadyExists(message="Batch already exists by reference.")

        current_date = get_now()

        expiry_date = self.batch.get('expiry_date', None)

        if expiry_date < current_date:
            raise LessThanCurrentDate()

    def start(self) -> Batch:
        self.batch_obj.save()

        return self.batch_obj

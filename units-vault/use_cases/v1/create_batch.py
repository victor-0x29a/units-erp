from datetime import datetime
from documents import Batch
from exceptions import AlreadyExists, LessThanCurrentDate


class CreateBatch:
    def __init__(self, data={}, batch_document: Batch = None):
        self.batch = data
        self.document = batch_document

        self.__validate()

    def __validate(self):
        batch = self.document.objects(reference=self.batch.get('reference', None))

        if batch:
            raise AlreadyExists(message="Batch already exists by reference.")

        expiry_date = self.batch.get('expiry_date', None)

        expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")

        current_date = datetime.now()

        if expiry_date < current_date:
            raise LessThanCurrentDate()

    def start(self):
        created_batch = self.document(**self.batch)

        created_batch.save()

        return created_batch

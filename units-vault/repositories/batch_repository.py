from documents import Batch
from exceptions import MissingParam, MissingDoc


class BatchRepository:
    def __init__(self, batch_document: Batch):
        self.Batch = batch_document

    def delete(self, batch: Batch) -> None:
        if not batch:
            raise MissingParam('Batch is required.')

        batch.delete()

    def get(self, filters=None, can_raises=True):
        if not filters:
            raise MissingParam("Filter is required.")

        batch = self.Batch.objects(**filters).first()

        if not batch and can_raises:
            raise MissingDoc("Batch not found.")

        return batch

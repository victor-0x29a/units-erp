from datetime import datetime
from mongoengine.errors import NotUniqueError
from documents import Batch
from exceptions import MissingParam, MissingDoc, LessThanCurrentDate, UniqueKey
from utils.dates import get_now


class BatchRepository:
    def __init__(self, batch_document: Batch):
        self.Batch = batch_document

    def create(self, data: dict) -> Batch:
        self.__validate_exp_date(exp_date=data.get('expiry_date'))

        try:
            batch = self.Batch(**data)

            batch.save()
        except NotUniqueError:
            raise UniqueKey('Batch already exists by reference.')

        return batch

    def delete(self, batch: Batch) -> None:
        if not batch:
            raise MissingParam('Batch is required.')

        batch.delete()

    def get(self, filters=None, can_raises=True, is_only_one=True) -> Batch | list[Batch]:
        if not filters:
            raise MissingParam("Filter is required.")

        batch = self.Batch.objects(**filters).first() if is_only_one else self.Batch.objects(**filters)

        if not batch and can_raises and is_only_one:
            raise MissingDoc("Batch not found.")

        return batch if is_only_one else list(batch)

    def __validate_exp_date(self, exp_date: datetime):
        if not exp_date:
            raise MissingParam('Expiry date is required.')

        now = get_now()

        if exp_date < now:
            raise LessThanCurrentDate()

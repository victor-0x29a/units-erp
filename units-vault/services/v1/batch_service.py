from documents import Batch
from use_cases import CreateBatchV1


class BatchService:
    def create(self, data={}):
        create_worker = CreateBatchV1(
            batch_document=Batch,
            data=data
        )

        create_worker.start()

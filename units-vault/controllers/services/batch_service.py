from datetime import datetime
from documents import Batch
from use_cases import CreateBatchV1


class BatchService:
    def create(self, data={}):
        data = data.dict()

        create_payload = {
            "expiry_date": datetime.strptime(data.get("expiry_date"), "%d/%m/%Y"),
            "inserction_datetime": datetime.now(),
            "supplier_document": data.get("cnpj"),
            "reference": data.get("ref")
        }

        create_worker = CreateBatchV1(
            batch_document=Batch,
            data=create_payload
        )

        create_worker.start()

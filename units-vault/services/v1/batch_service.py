from documents import Batch
from use_cases import CreateBatchV1
from utils import dates


class BatchService:
    def create(self, data={}):
        data = data.model_dump()

        create_payload = {
            "expiry_date": dates.parse_date(data.get("expiry_date")),
            "inserction_datetime": dates.get_now(),
            "supplier_document": data.get("cnpj"),
            "reference": data.get("ref")
        }

        create_worker = CreateBatchV1(
            batch_document=Batch,
            data=create_payload
        )

        create_worker.start()

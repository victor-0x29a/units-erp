from fastapi import APIRouter
from ..interfaces import CreateBatchV1
from services.v1.batch_service import BatchService
from utils import dates


router = APIRouter(prefix='/v1/batch')


@router.post('/', status_code=204, tags=['batch'])
def create_batch(payload: CreateBatchV1):
    data = payload.model_dump()

    create_payload = {
        "expiry_date": dates.parse_date(data.get("expiry_date")),
        "inserction_datetime": dates.get_now(),
        "supplier_document": data.get("cnpj"),
        "reference": data.get("ref")
    }

    service = BatchService()

    service.create(create_payload)

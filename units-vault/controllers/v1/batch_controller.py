from fastapi import APIRouter
from ..dto import CreateBatchV1
from services.v1.batch_service import BatchService
from utils.dates import from_str_to_date, get_now


router = APIRouter(prefix='/v1/batch')


@router.post('/', status_code=204, tags=['batch'])
def create_batch(payload: CreateBatchV1):
    data = payload.model_dump()

    create_payload = {
        "expiry_date": from_str_to_date(data.get("expiry_date")),
        "inserction_datetime": get_now(),
        "supplier_document": data.get("cnpj"),
        "reference": data.get("ref")
    }

    service = BatchService()

    service.create(create_payload)

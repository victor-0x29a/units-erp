from fastapi import APIRouter, Depends
from middlewares import create_auth_middleware
from services.v1.batch_service import BatchService
from utils.dates import from_str_to_date, get_now
from docs_constants import EMPLOYEE_ROLES
from ..dto import CreateBatchV1

router = APIRouter(prefix='/v1/batch')


@router.post(
    '/',
    status_code=204,
    tags=['batch'],
    dependencies=[
        Depends(
            create_auth_middleware(
                enabled_roles=[
                    EMPLOYEE_ROLES['inventor'],
                    EMPLOYEE_ROLES['financial']
                ]
            ))
    ])
def create_batch(payload: CreateBatchV1):
    data = payload.model_dump()

    create_payload = {
        "expiry_date": from_str_to_date(data.get("expiry_date")),
        "inserction_datetime": get_now(),
        "supplier_document": data.get("cnpj"),
        "reference": data.get("ref"),
        "store_unit": data.get("store_unit")
    }

    service = BatchService()

    service.create(create_payload)

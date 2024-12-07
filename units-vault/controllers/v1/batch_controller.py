from fastapi import APIRouter, Depends
from middlewares import create_auth_middleware
from services.v1.batch_service import BatchService
from services.v1.store_service import StoreService
from utils.dates import from_str_to_date, get_now
from docs_constants import EMPLOYEE_ROLES
from ..dto import CreateBatchV1

router = APIRouter(prefix='/v1/batch')

service = BatchService()
store_service = StoreService()


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

    service.create(create_payload)


@router.delete(
    '/{reference}',
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
def delete(reference: str):
    service.delete(reference=reference)


@router.get(
    '/{reference}',
    tags=['batch'],
    dependencies=[
        Depends(
            create_auth_middleware(
                enabled_roles=[
                    EMPLOYEE_ROLES['inventor'],
                    EMPLOYEE_ROLES['financial'],
                    EMPLOYEE_ROLES['operator']
                ]
            ))
    ])
def get(reference: str):
    batch_data = service.get(reference=reference)
    print(batch_data)
    store_unit = store_service.get(filter={"id": batch_data.store.id}).unit

    return {
        "reference": batch_data.reference,
        "inserction_datetime": batch_data.inserction_datetime,
        "expiry_date": batch_data.expiry_date,
        "store_unit": store_unit,
        "cnpj": batch_data.supplier_document
    }

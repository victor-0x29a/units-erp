from fastapi import APIRouter, Depends
from middlewares import create_auth_middleware
from services.v1.product_service import ProductService
from docs_constants import EMPLOYEE_ROLES
from ..dto import CreateProductV1


router = APIRouter(prefix="/v1/product")

service = ProductService()


@router.post(
    "/",
    status_code=204,
    tags=['product'],
    dependencies=[
        Depends(
            create_auth_middleware(
                enabled_roles=[
                    EMPLOYEE_ROLES['inventor'],
                    EMPLOYEE_ROLES['financial']
                ]
            ))
    ])
def create_product(payload: CreateProductV1):
    data = payload.model_dump()

    create_payload = {
        **data,
        "item_type": data.get("type"),
        "data_type": data.get("for_use"),
        "stock": data.get("base_stock")
    }

    create_payload.pop("type")
    create_payload.pop("for_use")
    create_payload.pop("base_stock")

    service.create(create_payload)


@router.delete(
    "/{bar_code}",
    status_code=204,
    tags=['product'],
    dependencies=[
        Depends(
            create_auth_middleware(
                enabled_roles=[
                    EMPLOYEE_ROLES['inventor'],
                    EMPLOYEE_ROLES['financial']
                ]
            ))
    ])
def delete(bar_code: int):
    service.delete(bar_code=str(bar_code))

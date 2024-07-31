from fastapi import APIRouter
from services.v1.product_service import ProductService
from ..interfaces import CreateProductV1


router = APIRouter(prefix="/v1/product")


@router.post("/", status_code=204, tags=['product'])
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

    service = ProductService()

    service.create(create_payload)

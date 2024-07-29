from fastapi import APIRouter
from services.v1.product_service import ProductService
from ..interfaces import CreateProductV1


router = APIRouter(prefix="/v1/product")


@router.post("/", status_code=204, tags=['product'])
def create_product(payload: CreateProductV1):
    service = ProductService()

    service.create(payload)

from fastapi import APIRouter
from services.product_service import ProductService
from .interfaces import CreateProductV1


router = APIRouter(prefix="/product")


@router.post("/", status_code=204)
def create_product(payload: CreateProductV1):
    service = ProductService()

    service.create(payload)

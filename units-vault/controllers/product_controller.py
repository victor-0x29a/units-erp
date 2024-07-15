from fastapi import APIRouter
from services.product_service import ProductService
from .interfaces import CreateProductV1


router = APIRouter(prefix="/product")


@router.post("/")
def create_product(payload: CreateProductV1):
    print(payload)
    return ProductService().create(payload)

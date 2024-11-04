from fastapi import APIRouter
from services.v1.store_service import StoreService as StoreServiceV1
from ..dto import CreateStoreV1


router = APIRouter(prefix="/v1/store")


@router.post("/", status_code=204, tags=['product'])
def create_product(payload: CreateStoreV1):
    data = payload.model_dump()

    service = StoreServiceV1()

    service.instance(data=data)

    service.create()

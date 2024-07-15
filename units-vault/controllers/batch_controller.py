from fastapi import APIRouter
from .interfaces import CreateBatchV1
from .services.batch_service import BatchService


router = APIRouter(prefix="/batch")


@router.post("/", status_code=204)
def create_batch(payload: CreateBatchV1):
    service = BatchService()

    service.create(payload)

from fastapi import APIRouter
from ..interfaces import CreateBatchV1
from services.v1.batch_service import BatchService


router = APIRouter(prefix='/v1/batch')


@router.post('/', status_code=204, tags=['batch'])
def create_batch(payload: CreateBatchV1):
    service = BatchService()

    service.create(payload)

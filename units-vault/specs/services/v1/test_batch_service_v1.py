from services.v1.batch_service import BatchService
from repositories import StoreRepository
from documents import Store
from datetime import timedelta
from utils.dates import get_now
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.constants import company_doc


class TestCreateBatch:
    def test_should_create(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        service = BatchService()

        create_payload = {
            "reference": "REFERER001",
            "inserction_datetime": get_now(),
            "expiry_date": get_now() + timedelta(days=1),
            "store_unit": 1,
            "supplier_document": company_doc
        }

        service.create(data=create_payload)

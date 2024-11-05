from fastapi import APIRouter
from services.v1.store_service import StoreService as StoreServiceV1
from ..dto import CreateStoreV1, UpdateStoreV1


router = APIRouter(prefix="/v1/store")


@router.post("/", status_code=204, tags=['store'])
def create_store(payload: CreateStoreV1):
    data = payload.model_dump()

    service = StoreServiceV1()

    service.instance(data=data)

    service.create()


@router.delete("/{unit}", status_code=204, tags=['store'])
def delete_store(unit: int):
    service = StoreServiceV1()

    service.delete(unit=int(unit))


@router.get("/{unit}", tags=['store'])
def get_store(unit: int):
    service = StoreServiceV1()

    store = service.get(filter={"unit": int(unit)})

    parsed_store = store._data

    parsed_store.pop("id")

    return parsed_store


@router.put("/{unit}", status_code=204, tags=['store'])
def update_store(unit: int, payload: UpdateStoreV1):
    data = payload.model_dump()

    service = StoreServiceV1()

    service.update(unit=int(unit), data_for_update=data)

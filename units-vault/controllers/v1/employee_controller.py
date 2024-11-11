from fastapi import APIRouter
from services.v1.employee_service import EmployeeService as EmployeeServiceV1
from ..dto import CreateEmployeeV1


router = APIRouter(prefix="/v1/employee")


@router.post("/", status_code=204, tags=['employee'])
def create_employee(payload: CreateEmployeeV1):
    data = payload.model_dump()

    employee_service = EmployeeServiceV1()

    parsed_data = {
        **data
    }

    parsed_data['store_unit'] = data.get('store')
    parsed_data['name'] = data.get('full_name')

    parsed_data.pop('store')

    parsed_data.pop('full_name')

    employee_service.create(data=parsed_data)


@router.delete("/{employee_doc}", status_code=204, tags=['employee'])
def delete_employee(employee_doc: str):
    employee_service = EmployeeServiceV1()

    employee_service.delete(employee_document=employee_doc)

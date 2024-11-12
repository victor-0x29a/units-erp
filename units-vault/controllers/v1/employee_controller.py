from fastapi import APIRouter, Depends
from fastapi.responses import Response
from middlewares import create_auth_middleware
from services.v1.employee_service import EmployeeService as EmployeeServiceV1
from docs_constants import EMPLOYEE_ROLES
from ..dto import CreateEmployeeV1, FillPasswordV1, LoginV1


router = APIRouter(prefix="/v1/employee")


@router.post(
    "/",
    status_code=204,
    tags=['employee'],
    dependencies=[Depends(create_auth_middleware(enabled_roles=[EMPLOYEE_ROLES['admin']]))])
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


@router.delete(
    "/{employee_doc}",
    status_code=204,
    tags=['employee'],
    dependencies=[Depends(create_auth_middleware(enabled_roles=[EMPLOYEE_ROLES['admin']]))])
def delete_employee(employee_doc: str):
    employee_service = EmployeeServiceV1()

    employee_service.delete(employee_document=employee_doc)


@router.put(
    "/{employee_doc}/password",
    status_code=204,
    tags=['employee'],
    dependencies=[Depends(create_auth_middleware())])
def fill_password(employee_doc: str, payload: FillPasswordV1):
    parsed_payload = payload.model_dump()

    employee_service = EmployeeServiceV1()

    employee_service.fill_password(
        employee_document=employee_doc,
        password=parsed_payload['password']
    )


@router.post("/login", status_code=204, tags=['employee'])
def login(payload: LoginV1):
    parsed_payload = payload.model_dump()

    employee_service = EmployeeServiceV1()

    token = employee_service.login(
        username=parsed_payload.get('username', None),
        document=parsed_payload.get('document', None),
        password=parsed_payload['password']
    )

    return Response(headers={"Authorization": token}, status_code=204)

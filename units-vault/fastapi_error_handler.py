from fastapi import Request
from fastapi.responses import JSONResponse, Response
from exceptions import exceptions_code, VALIDATION_ERROR_CODE
from mongoengine import ValidationError
from documents import Batch
from docs_constants import DOCS_DTO


def parse_errors(exc, is_fastapi_validation_error=False):
    parsed_errors = []

    if is_fastapi_validation_error:
        errors = exc._errors

        for error in errors:
            loc = error.get('loc', [])

            parsed_errors.append({
                "field": loc[1] if len(loc) > 1 else 'N/A',
                "message": error.get('msg')
            })

        return parsed_errors

    batch_fields = Batch._fields

    supplier_field = batch_fields.get('supplier_document').name

    for key, value in exc.items():
        if key == supplier_field:
            key = DOCS_DTO.get(supplier_field)

        parsed_errors.append({
            "field": key,
            "message": value._message
        })

    return parsed_errors


def can_show_internal_error(exc: Exception):
    is_mongo_exception = exc.__class__.__module__.startswith("mongoengine")

    if is_mongo_exception:
        return True

    has_message_attr = hasattr(exc, "message")

    has_code_attr = hasattr(exc, "code")

    if not has_message_attr or not has_code_attr:
        return True

    return False


def mount_template_response(
    code=0,
    message="Internal Server Error",
    errors=[],
    status_code=500
):
    if status_code == 500:
        return Response(status_code=500)

    return JSONResponse({
        "code": code,
        "message": message,
        "errors": errors
    }, status_code=status_code)


"""
TEMPLATE FROM `unhandled_exceptions` RESPONSE METHOD


MESSAGE: STR
CODE: INT
ERRORS: ANY[]
"""


async def unhandled_exceptions(request: Request, exc: Exception):
    is_validation_error = isinstance(exc, ValidationError)

    if is_validation_error:
        exception_details = exceptions_code.get(VALIDATION_ERROR_CODE)

        return mount_template_response(
            message=exception_details.get("message"),
            status_code=exception_details.get("http"),
            code=VALIDATION_ERROR_CODE,
            errors=parse_errors(exc.errors)
        )

    if can_show_internal_error(exc):
        return mount_template_response()

    message = exc.message

    code = exc.code

    status_code = exceptions_code.get(code, {}).get("http", 500)

    return mount_template_response(
        code=code,
        message=message,
        status_code=status_code
    )


async def http_exceptions(request: Request, exc: Exception):
    exception_details = exceptions_code.get(VALIDATION_ERROR_CODE)
    parsed_errors = parse_errors(
        exc,
        is_fastapi_validation_error=True
    )

    return mount_template_response(
        code=VALIDATION_ERROR_CODE,
        errors=parsed_errors,
        message=exception_details.get('message'),
        status_code=exception_details.get('http')
    )

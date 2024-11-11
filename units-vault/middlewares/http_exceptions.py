from fastapi import Request
from exceptions import exceptions_code, VALIDATION_ERROR_CODE
from .utils import get_response_template, parse_errors


async def http_exceptions(request: Request, exc: Exception):
    exception_details = exceptions_code.get(VALIDATION_ERROR_CODE)
    parsed_errors = parse_errors(
        exc,
        is_fastapi_validation_error=True
    )

    return get_response_template(
        code=VALIDATION_ERROR_CODE,
        errors=parsed_errors,
        message=exception_details.get('message'),
        status_code=exception_details.get('http')
    )

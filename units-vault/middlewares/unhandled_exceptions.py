from fastapi import Request
from exceptions import exceptions_code, VALIDATION_ERROR_CODE
from mongoengine import ValidationError
from .utils import get_response_template, parse_errors


def can_show_internal_error(exc: Exception):
    is_mongo_exception = exc.__class__.__module__.startswith("mongoengine")

    if is_mongo_exception:
        return True

    has_message_attr = hasattr(exc, "message")

    has_code_attr = hasattr(exc, "code")

    if not has_message_attr or not has_code_attr:
        return True

    return False


async def unhandled_exceptions(request: Request, exc: Exception):
    is_validation_error = isinstance(exc, ValidationError)

    if is_validation_error:
        exception_details = exceptions_code.get(VALIDATION_ERROR_CODE)

        return get_response_template(
            message=exception_details.get("message"),
            status_code=exception_details.get("http"),
            code=VALIDATION_ERROR_CODE,
            errors=parse_errors(exc.errors)
        )

    if can_show_internal_error(exc):
        return get_response_template()

    message = exc.message

    code = exc.code

    status_code = exceptions_code.get(code, {}).get("http", 500)

    return get_response_template(
        code=code,
        message=message,
        status_code=status_code
    )

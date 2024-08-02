from fastapi import Request
from fastapi.responses import JSONResponse, Response
from exceptions import exceptions_code


async def unhandled_exceptions(request: Request, exc: Exception):
    internal_server_error_label = "Internal server error."

    is_mongo_exception = exc.__class__.__module__.startswith("mongoengine")

    if is_mongo_exception:
        return Response(status_code=500)

    try:
        message = exc.message
    except Exception:
        message = internal_server_error_label

    try:
        code = exc.__getattribute__("code")
    except Exception:
        code = 500

    status_code = exceptions_code.get(code, {}).get("http", 500)
    return JSONResponse({
        "message": message
    }, status_code=status_code)

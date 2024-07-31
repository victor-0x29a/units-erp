from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import exceptions_code


async def unhandled_exceptions(request: Request, exc: Exception):
    try:
        message = exc.message
    except Exception:
        message = "Internal server error."

    status_code = exceptions_code.get(exc.code, {}).get("http", 500)
    return JSONResponse({
        "message": message
    }, status_code=status_code)

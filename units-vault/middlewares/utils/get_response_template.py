from fastapi.responses import JSONResponse, Response


def get_response_template(
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

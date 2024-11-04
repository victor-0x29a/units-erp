VALIDATION_ERROR_CODE = 999

exceptions_code = {
    500: {
        "http": 500
    },
    1003: {
        "http": 404
    },
    1001: {
        "http": 400
    },
    1002: {
        "http": 409
    },
    1009: {
        "http": 406
    },
    1010: {
        "http": 409
    },
    1011: {
        "http": 422
    },
    VALIDATION_ERROR_CODE: {
        "http": 422,
        "message": "Validation error"
    }
}

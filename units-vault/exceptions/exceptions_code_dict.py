VALIDATION_ERROR_CODE = 999
UNIQUE_KEY_ERROR_CODE = 1000

exceptions_code = {
    1003: {
        "http": 409
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
    VALIDATION_ERROR_CODE: {
        "http": 422,
        "message": "Validation error"
    },
    UNIQUE_KEY_ERROR_CODE: {
        "http": 409,
        "message": "Unique key error"
    }
}

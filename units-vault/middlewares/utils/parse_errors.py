from documents import Batch
from docs_constants import DOCS_DTO


def parse_errors(exc, is_fastapi_validation_error=False):
    parsed_errors = []

    if is_fastapi_validation_error:
        errors = exc._errors

        for error in errors:
            loc = error.get('loc', [])

            loc_error = loc[1] if len(loc) > 1 else 'N/A'

            if loc_error == 'N/A':
                # TO DO: identify the reason for this case (try send a request with a wrong JSON payload)
                print(error)

            parsed_errors.append({
                "field": loc_error,
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

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


def create_test_client(app):
    magic_constants = MagicMock()

    magic_constants.JWT_ALGORITHM = 'HS256'

    with patch.dict('sys.modules', {'constants': magic_constants}):
        from security import SignatureManager

    signature_manager = SignatureManager(secret='secret')

    token = signature_manager.sign(payload={
        'employee_role': 'ADMIN',
        'employee_document': '000005',
        'store_unit': 1
    })

    def gen_test_client():
        return TestClient(app, headers={
            'Authorization': token
        })

    return gen_test_client()

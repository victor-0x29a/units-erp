from fastapi import Request, Response
from security import SignatureManager
from exceptions import MissingAuthorization, MissingPermission
from constants import JWT_SECRET
from docs_constants import EMPLOYEE_ROLES


signature_manager = SignatureManager(secret=JWT_SECRET)


def create_auth_middleware(enabled_roles: list = []):
    def validate_authentication(request: Request, response: Response):
        token = request.headers.get("Authorization")

        if not token:
            raise MissingAuthorization()

        is_valid_authorization = signature_manager.verify_signature(token=token)

        if not is_valid_authorization:
            raise MissingAuthorization()

        decoded_token = signature_manager.decode_signature(token=token)

        is_admin = decoded_token['employee_role'] == EMPLOYEE_ROLES['admin']

        if not is_admin:
            is_in_enabled_roles = decoded_token['employee_role'] in enabled_roles

            if not is_in_enabled_roles:
                raise MissingPermission()

    return validate_authentication

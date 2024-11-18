import jwt
from datetime import timedelta
from utils.dates import get_now
from constants import JWT_ALGORITHM


class SignatureManager:
    def __init__(self, secret):
        self.__secret = secret

    def sign(self, payload: dict = {}, is_temporary=False):
        signature_payload = {
            'iat': int(get_now().timestamp()),
            'exp': self.__gen_expiry_date(is_temporary=is_temporary, hours=2),
            'is_temporary': is_temporary,
            **payload
        }

        return jwt.encode(signature_payload, self.__secret, algorithm=JWT_ALGORITHM)

    def decode_signature(self, token: str):
        return jwt.decode(token, self.__secret, algorithms=[JWT_ALGORITHM])

    def verify_signature(self, token: str):
        try:
            jwt.decode(
                token,
                self.__secret,
                algorithms=[JWT_ALGORITHM],
                verify=True
            )
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        except jwt.InvalidSignatureError:
            return False
        except jwt.DecodeError:
            return False

        return False

    def __gen_expiry_date(self, is_temporary=False, hours=2):
        token_hour_duration = hours if not is_temporary else 0
        token_minute_duration = 10 if is_temporary else 0

        datetime = get_now() + timedelta(
            hours=token_hour_duration,
            minutes=token_minute_duration
        )

        return int(datetime.timestamp())

import jwt
from datetime import timedelta
from utils.dates import get_now
from constants import JWT_ALGORITHM


class SignatureManager:
    def __init__(self, secret):
        self.__secret = secret

    def sign(self, payload: dict = {}):
        signature_payload = {
            'iat': int(get_now().timestamp()),
            'exp': self.__gen_expiry_date(),
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

    def __gen_expiry_date(self, hours=2):
        datetime = get_now() + timedelta(hours=hours)
        return int(datetime.timestamp())

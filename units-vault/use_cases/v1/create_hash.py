import bcrypt
import base64
import hashlib


class CreateHash:
    def __encode(self, content: str):
        encoded_content = content.encode('utf-8')
        return base64.b64encode(hashlib.sha256(encoded_content).digest())

    def hash_passwd(self, content: str):
        salts = bcrypt.gensalt()

        content_encoded = self.__encode(content=content)

        return bcrypt.hashpw(content_encoded, salts).decode('utf-8')

    def is_valid_hash_comparison(self, content: str, hashed: str) -> bool:
        content_encoded = self.__encode(content=content)

        hashed_bytes = hashed.encode('utf-8')

        return bcrypt.checkpw(content_encoded, hashed_bytes)

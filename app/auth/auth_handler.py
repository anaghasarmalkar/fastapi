import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


class JWTException(Exception):
    def __init__(self, message: str):
        self.message = message


def sign_jwt(username: str) -> Dict[str, str]:
    payload = {
        "username": username,
        # expiry time of ten minutes from when it is generated
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token
        else:
            raise JWTException("Token expired. Get new one")
    except jwt.ExpiredSignatureError:
        raise JWTException("Token expired. Get new one")
    except jwt.InvalidTokenError:
        raise JWTException("Invalid Token")

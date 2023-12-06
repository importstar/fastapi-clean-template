import datetime
import pyotp

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import AuthError
from app.repository.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

OTP = pyotp.HOTP(
    pyotp.random_base32(
        chars="".join(c for c in settings.SECRET_KEY if c.isalpha() or c.isdigit())
    ),
    # interval=settings.OTP_INTERVAL,
)


def create_access_token(
    subject: dict, expires_delta: datetime.timedelta = None
) -> tuple[str, datetime.datetime]:
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    expire = expire.replace(microsecond=0)
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    # expiration_datetime = str(int(expire.timestamp()))
    return encoded_jwt, expire


def create_refresh_token(
    subject: dict, expires_delta: datetime.timedelta = None
) -> tuple[str, datetime.datetime]:
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    expire = expire.replace(microsecond=0)
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    # expiration_datetime = str(int(expire.timestamp()))
    return encoded_jwt, expire


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str) -> dict:
    try:
        user_repository = UserRepository()
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        user = user_repository.get_by_id(decoded_token["id"])
        user_token = user_repository.get_token(user)

        return (
            decoded_token
            if decoded_token["exp"] == user_token.access_token_expires.timestamp()
            else None
        )
    except Exception as e:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError("Invalid authentication scheme.")

            if not self.verify_jwt(credentials.credentials):
                raise AuthError("Invalid token or expired token.")

            return credentials.credentials
        else:
            raise AuthError("Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid

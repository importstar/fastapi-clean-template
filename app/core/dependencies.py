from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from app.core.settings import settings
from app.core.exceptions import AuthError
from app.core.security import ALGORITHM, JWTBearer
from app.models.user_model import User
from app.schemas.auth_schema import Payload
from app.services.user_service import UserService


def get_current_user(
    token: str = Depends(JWTBearer()),
) -> User:
    service = UserService()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        raise AuthError(detail="User not found")
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


def get_current_user_with_no_exception(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(UserService),
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        return None
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        return None
    return current_user


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    # if not current_user.is_superuser:
    #     raise AuthError("It's not a super user")
    return current_user

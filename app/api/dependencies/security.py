from fastapi import (
    Depends,
    HTTPException,
    status
)
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes
)
from jose import jwt, JWTError
from pydantic import ValidationError

from app.config import settings
from app.api.scopes import SCOPES
from app.services.users import UsersService
from app.api.dependencies.common import get_service
from app.schemas.users import (
    UserSchema,
    TokenSchema
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.SECURITY_ACCESS_TOKEN_URL,
    scopes=SCOPES
)


def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
        user: UsersService = Depends(get_service(UsersService))
) -> UserSchema:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value}
    )
    try:
        payload = jwt.decode(token, settings.SECURITY_SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token = TokenSchema(scopes=payload.get("scopes", []), username=username)

        user_data = user.get_by_username(token.username)

        if user_data is None:
            raise credentials_exception

        user_data = UserSchema.from_orm(user_data)
    except (JWTError, ValidationError):
        raise credentials_exception

    # Check permissions
    if "admin" not in token.scopes:
        for scope in security_scopes.scopes:
            if scope not in token.scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value}
                )
    return user_data

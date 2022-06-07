from typing import Optional
from datetime import (
    datetime,
    timedelta
)

from fastapi import (
    APIRouter,
    Response,
    Request,
    Depends,
    HTTPException,
    Cookie,
    Security,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.config import settings
from app.models.models import Users
from app.services.users import UsersService
from app.api.dependencies.common import get_service
from app.api.dependencies.security import get_current_user
from app.lib.security import verify_password, get_password_hash
from app.lib.folders import create_main_dir
from app.schemas.users import (
    TokenResponseSchema,
    UserSchema,
    UserRegisterSchema
)


router = APIRouter()


def create_token(data: dict, expires_delta: timedelta):
    data_copy = data.copy()
    expire = datetime.utcnow() + expires_delta
    data_copy.update({"exp": expire})
    encoded = jwt.encode(data_copy, settings.SECURITY_SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded


def create_user_tokens(user: Users):
    access_token_expires = timedelta(minutes=settings.SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.SECURITY_REFRESH_TOKEN_EXPIRE_MINUTES)

    # Create access token
    access_token = create_token(
        data={
            "sub": user.username,
            "scopes": user.scopes
        },
        expires_delta=access_token_expires
    )
    # Create refresh token
    refresh_token = create_token(
        data={
            "sub": user.username
        },
        expires_delta=refresh_token_expires
    )

    return access_token, refresh_token


def set_refresh_token_cookie(response: Response, token: str):
    response.set_cookie(
        key=settings.SECURITY_REFRESH_TOKEN_COOKIE_KEY,
        value=token,
        expires=settings.SECURITY_REFRESH_TOKEN_COOKIE_EXPIRES,
        path=settings.SECURITY_REFRESH_TOKEN_COOKIE_PATH,
        domain=settings.SECURITY_REFRESH_TOKEN_COOKIE_DOMAIN,
        httponly=settings.SECURITY_REFRESH_TOKEN_COOKIE_HTTPONLY,
        secure=settings.SECURITY_REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.SECURITY_REFRESH_TOKEN_COOKIE_SAMESITE
    )


# Register new user
@router.post(
    "/register",
    name="users:register"
)
def register_user(
        user_data: UserRegisterSchema,
        user: UsersService = Depends(get_service(UsersService)),
):
    # Check if user with same username exist
    if user.get_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with same username exist"
        )
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    # Create new user
    user.create_user(
        user_data.username,
        hashed_password,
        user_data.full_name,
        age=user_data.age
    )
    # Create main root
    user_id = user.get_by_username(user_data.username).id
    create_main_dir(user_id)
    return {"message": "User successfully created"}


# Generate the access token
@router.post(
    "/login",
    response_model=TokenResponseSchema,
    name="users:login"
)
def login_users(
        request: Request,
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        user: UsersService = Depends(get_service(UsersService))
):
    # Check if user data is correct
    user_data = user.get_by_username(form_data.username)
    if not (user_data and verify_password(form_data.password, user_data.password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad data!")
    access_token, refresh_token = create_user_tokens(user_data)
    # Set cookie
    set_refresh_token_cookie(response, refresh_token)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Refresh access token
@router.post(
    "/token/refresh",
    response_model=TokenResponseSchema,
    name="users:refresh-token"
)
def refresh_token(
        request: Request,
        response: Response,
        token: Optional[str] = Cookie(None, alias=settings.SECURITY_REFRESH_TOKEN_COOKIE_KEY),
        user: UsersService = Depends(get_service(UsersService))
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token"
    )
    if token is None:
        raise credentials_exception
    # Try to get username from refresh token
    try:
        payload = jwt.decode(token, settings.SECURITY_SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Get user
    user_data = user.get_by_username(username)

    if user_data is None:
        raise credentials_exception

    access_token, refresh_token = create_user_tokens(user_data)

    set_refresh_token_cookie(response, refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Logout
@router.post(
    "/logout",
    name="users:logout"
)
def logout(
        response: Response,
        user: UserSchema = Security(get_current_user)
):
    response.delete_cookie(
        settings.SECURITY_REFRESH_TOKEN_COOKIE_KEY,
        settings.SECURITY_REFRESH_TOKEN_COOKIE_PATH,
        settings.SECURITY_REFRESH_TOKEN_COOKIE_DOMAIN
    )
    return {}

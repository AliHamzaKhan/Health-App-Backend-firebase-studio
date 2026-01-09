from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.api.v1 import deps
from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.crud.crud_user import crud_user
from app.schemas.token import Token
from app.schemas.user import User
from app.schemas.response import StandardResponse

settings = get_settings()
router = APIRouter()


class LoginResponse(BaseModel):
    token: Token
    user: User


@router.post("/login/access-token", response_model=StandardResponse[LoginResponse])
async def login_access_token(
        db: AsyncSession = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        return StandardResponse(success=False, message="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add user id and role to the token payload for use in dependencies
    token_data = {"sub": user.email, "user_id": user.id, "role": user.role}
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    token = Token(access_token=access_token, token_type="bearer")
    
    # The User schema should be configured to not include the hashed_password
    login_data = LoginResponse(token=token, user=user)

    return StandardResponse(data=login_data, message="Login successful")

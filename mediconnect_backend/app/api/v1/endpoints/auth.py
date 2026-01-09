from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.api.v1 import deps
from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.crud.crud_user import crud_user
from app.schemas.token import Token
from app.schemas.user import User, UserCreate, UserLoginResponse
from app.schemas.response import StandardResponse
from app import crud

settings = get_settings()
router = APIRouter()


class LoginResponse(BaseModel):
    token: Token
    user: UserLoginResponse


@router.post("/login/access-token", response_model=StandardResponse[LoginResponse])
async def login_access_token(
        db: AsyncSession = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud_user.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        return StandardResponse(success=False, message="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token_data = {"sub": user.email, "user_id": user.id, "role": user.role.role}
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    token = Token(access_token=access_token, token_type="bearer")
    
    user_data = UserLoginResponse(
        **user.__dict__,
        date_of_birth=user.patient_profile.date_of_birth if user.patient_profile else None,
        gender=user.patient_profile.gender if user.patient_profile else None,
        blood_type=user.patient_profile.blood_type if user.patient_profile else None,
        height=user.patient_profile.height if user.patient_profile else None,
        weight=user.patient_profile.weight if user.patient_profile else None,
        emergency_contact_name=user.patient_profile.emergency_contact_name if user.patient_profile else None,
        emergency_contact_phone=user.patient_profile.emergency_contact_phone if user.patient_profile else None,
        role_id=user.role.id,
        status=user.status,
        is_active=user.is_active
    )
    login_data = LoginResponse(token=token, user=user_data)

    return StandardResponse(data=login_data, message="Login successful")

@router.post("/signup", response_model=StandardResponse[User])
async def signup(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> dict:
    """
    Create new user without the need for a token.
    """
    user = await crud.crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    new_user = await crud.crud_user.create(db, obj_in=user_in)

    if user_in.allergies:
        for allergy_name in user_in.allergies:
            await crud.crud_allergy.create(db, obj_in={"name": allergy_name, "user_id": new_user.id})

    if user_in.medical_conditions:
        for condition_name in user_in.medical_conditions:
            await crud.crud_medical_condition.create(db, obj_in={"name": condition_name, "user_id": new_user.id})
    
    role = await crud.crud_role.get(db, id=user_in.role_id)

    if role and role.role == 'patient':
        patient_data = {
            "user_id": new_user.id,
            "date_of_birth": user_in.date_of_birth,
            "gender": user_in.gender,
            "blood_type": user_in.blood_type,
            "height": user_in.height,
            "weight": user_in.weight,
            "emergency_contact_name": user_in.emergency_contact_name,
            "emergency_contact_phone": user_in.emergency_contact_phone
        }
        await crud.crud_patient.create(db, obj_in=patient_data)

    return StandardResponse(data=new_user, message="User created successfully.")

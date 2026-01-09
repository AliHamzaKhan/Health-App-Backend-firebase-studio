from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schemas.role import Role

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    profile_pic: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_id: int
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    allergies: Optional[List[str]] = []
    medical_conditions: Optional[List[str]] = []
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    profile_pic: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[int] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    id: int
    status: Optional[int] = None
    is_active: bool
    role: Role

    class Config:
        from_attributes = True

class User(UserInDBBase):
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class UserInDB(UserInDBBase):
    hashed_password: str

class UserLoginResponse(User):
    role_id: int
    status: Optional[int] = None
    is_active: bool

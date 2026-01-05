from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    profile_pic: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    token_balance: Optional[int] = None

class UserInDBBase(UserBase):
    id: int
    role: str
    profile_pic: str | None = None
    phone: str | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

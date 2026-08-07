# from pydantic import BaseModel

# class User(BaseModel):
#     id: int
#     name: str
#     email: str
#     password: str
#     username: str = None
#     is_active: bool = True
#     is_admin: bool = False
#     is_verified: bool = False
#     created_at: str = None
#     updated_at: str = None
#     last_login: str = None
#     profile_picture: str = None
#     bio: str = None

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
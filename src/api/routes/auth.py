from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controller.auth_controller import (
    register,
    login,
    logout,
    change_password,
)

from src.api.database.database import get_db
from src.api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    LogoutResponse,
    ChangePasswordRequest,
)

from src.api.security.dependencies import (
    get_current_user,
)
from src.api.models.user import User

router = APIRouter()

#register route
@router.post("/register")
async def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return await register(request, db)

#login route
@router.post("/login")
async def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return await login(request, db)

#logout route
@router.post(
    "/logout",
    response_model=LogoutResponse,
)
async def logout_user(
    request: RefreshTokenRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return await logout(
        current_user.id,
        request.refresh_token,
        db,
    )
    
#change password route
@router.post(
    "/change-password",
)
async def change_user_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    return await change_password(
        current_user.id,
        request,
        db,
    )
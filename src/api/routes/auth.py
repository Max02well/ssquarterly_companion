from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controller.auth_controller import (
    login,
    register,
)
from src.api.database.database import get_db
from src.api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)


router = APIRouter()


@router.post("/register")
async def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return await register(request, db)


@router.post("/login")
async def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return await login(request, db)
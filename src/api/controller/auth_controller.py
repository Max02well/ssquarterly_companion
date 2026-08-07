from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.api.services.auth_service import AuthService

#register a new user
async def register(
    request,
    db: Session,
):
    service = AuthService(db)

    user = service.register(request)

    return {
        "message": "Registration successful.",
        "user": user,
    }

#login a user
async def login(
    request,
    db: Session,
):
    service = AuthService(db)
    return service.login(request)

#logout a user
async def logout(
    user_id: int,
    refresh_token: str,
    db: Session,
):
    service = AuthService(db)
    return service.logout(
        user_id,
        refresh_token,
    )

#change password
async def change_password(
    user_id: int,
    request,
    db: Session,
):
    service = AuthService(db)
    return service.change_password(
        user_id=user_id,
        current_password=request.current_password,
        new_password=request.new_password,
    )
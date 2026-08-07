from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.api.schemas.user import (
    UserCreate,
    UserUpdate,
)
from src.api.services.user_service import UserService


class UserController:

    # -----------------------------------------
    # Get all users
    # -----------------------------------------
    @staticmethod
    def get_users(db: Session):
        service = UserService(db)
        return service.get_users()

    # -----------------------------------------
    # Get user
    # -----------------------------------------
    @staticmethod
    def get_user(
        db: Session,
        user_id: int,
    ):
        service = UserService(db)
        user = service.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    # -----------------------------------------
    # Get current user
    # -----------------------------------------
    @staticmethod
    def get_me(
        db: Session,
        user_id: int,
    ):

        service = UserService(db)
        user = service.get_me(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    # -----------------------------------------
    # Create user
    # -----------------------------------------
    @staticmethod
    def create_user(
        db: Session,
        request: UserCreate,
    ):
        service = UserService(db)
        existing = service.get_user_by_email(
            request.email
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )
        return service.create_user(request)

    # -----------------------------------------
    # Update user
    # -----------------------------------------
    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        request: UserUpdate,
    ):
        service = UserService(db)
        # Check email collision
        if request.email:
            existing = service.get_user_by_email(
                request.email
            )
            if (
                existing
                and existing.id != user_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists",
                )

        user = service.update_user(
            user_id,
            request,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    # -----------------------------------------
    # Delete user
    # -----------------------------------------
    @staticmethod
    def delete_user(
        db: Session,
        user_id: int,
    ):

        service = UserService(db)

        user = service.delete_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return {
            "message": "Account deleted successfully"
        }
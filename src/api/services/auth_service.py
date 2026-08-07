from datetime import timedelta, datetime

from src.api.models.user import User
from src.api.schemas.auth import LoginResponse
from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from src.api.models.user import User
from src.api.repository.user_repository import UserRepository
from src.api.repository.refresh_token_repository import RefreshTokenRepository

from src.api.security.password import (
    hash_password,
    verify_password,
)

from src.api.schemas.auth import (
    LoginResponse,
)

from src.api.security.jwt import (
    create_access_token,
    create_refresh_token,
)


class AuthService:

    def __init__(self, db):

        self.db = db
        self.user_repo = UserRepository(db)
        self.refresh_repo = RefreshTokenRepository(db)
        
    #register a new user
    def register(self, request):

        existing = self.user_repo.get_by_email(
            request.email
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists."
            )

        user = User(
            email=request.email,
            password_hash=hash_password(
                request.password
            ),
            first_name=request.first_name,
            last_name=request.last_name,
        )

        return self.user_repo.create(user)
    
    #login a user
    def login(self, request):

        user = self.user_repo.get_by_email(
            request.email
        )

        if not user:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )

        valid = verify_password(
            request.password,
            user.password_hash,
        )

        if not valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access = create_access_token(
            user.id
        )

        refresh = create_refresh_token(
            user.id
        )
        
        expires_at = (
            datetime.utcnow()
            + timedelta(days=30)
        )
        self.refresh_repo.create(
            user.id,
            refresh,
            expires_at=expires_at,
        )

        return LoginResponse(
            access_token=access,
            refresh_token=refresh,
            token_type="Bearer",
            user=user
        )
    
    #logout a user
    def logout(self, user_id:int, refresh_token:str):
        token = self.refresh_repo.find_valid_token(
            user_id,
            refresh_token,
        )

        if not token:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        self.refresh_repo.revoke(token)

        return {
            "message": "Logged out successfully"
        }
    
    #change password
    def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str,
    ):
        user = self.user_repo.get_by_id(
            user_id
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not verify_password(
            current_password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        user.password_hash = hash_password(
            new_password
        )

        self.user_repo.update(user)
        # invalidate existing refresh tokens
        self.refresh_repo.revoke_all_for_user(
            user.id
        )

        return {
            "message": "Password changed successfully"
        }
    
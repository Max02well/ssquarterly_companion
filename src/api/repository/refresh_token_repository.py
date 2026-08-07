from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.models.refresh_token import RefreshToken
from src.api.security.password import (
    hash_password,
    verify_password,
)

class RefreshTokenRepository:

    def __init__(self, db):
        self.db = db
    #create a new refresh token
    def create(
        self,
        user_id: int,
        refresh_token: str,
        expires_at: datetime,
    ):
        token = RefreshToken(
            user_id=user_id,
            token_hash=hash_password(refresh_token),
            expires_at= expires_at
        )
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
    
    #get all active tokens for a user
    def get_active_tokens(
        self,
        user_id: int,
    ):
        return self.db.scalars(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > datetime.utcnow(),
            )
        ).all()
        
    #find a valid token for a user
    def find_valid_token(
        self,
        user_id: int,
        refresh_token: str,
    ):
        tokens = self.get_active_tokens(user_id)
        for token in tokens:
            if verify_password(
                refresh_token,
                token.token_hash,
            ):
                return token
        return None
    
    #revoke a specific token
    def revoke(
        self,
        token: RefreshToken,
    ):
        token.revoked_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(token)
        return token
    
    #revoke all tokens for a user
    def revoke_all_for_user(
        self,
        user_id: int,
    ):
        tokens = self.get_active_tokens(user_id)
        for token in tokens:
            token.revoked_at = datetime.utcnow()

        self.db.commit()
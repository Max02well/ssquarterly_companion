from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.models.user import User
from src.api.schemas.user import UserCreate


class UserService:

    @staticmethod
    def get_users(db: Session):
        result = db.execute(
            select(User)
        )

        return result.scalars().all()

    @staticmethod
    def get_user(
        db: Session,
        user_id: int,
    ):
        return db.get(User, user_id)

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str,
    ):
        result = db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    @staticmethod
    def create_user(
        db: Session,
        user_data: UserCreate,
    ):
        user = User(
            email=user_data.email,
            password_hash=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
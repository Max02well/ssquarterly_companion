from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.models.user import User
from src.api.schemas.user import UserCreate, UserUpdate
from src.api.security.password import hash_password
from src.api.repository.user_repository import UserRepository

class UserService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)
    
    #get all users
    def get_users(self):
        return self.user_repo.get_all()
    
    #get a user by id
    def get_user(self, user_id: int):
        return self.user_repo.get_by_id(user_id)
    
    #get a user by email
    #     db: Session,
    #     email: str,
    # ):
    #     result = db.execute(
    #         select(User).where(User.email == email)
    #     )

    #     return result.scalar_one_or_none()
    def get_user_by_email(self, email: str):
        return self.user_repo.get_by_email(email)
    
    #get current user
    def get_me(self, user_id: int):
        return self.user_repo.get_by_id(user_id)
    
    
    #create a new user
    # @staticmethod
    # def create_user(
    #     db: Session,
    #     user_data: UserCreate,
    # ):
    #     user = User(
    #         email=user_data.email,
    #         password_hash=hash_password(user_data.password),
    #         first_name=user_data.first_name,
    #         last_name=user_data.last_name,
    #     )

    #     db.add(user)
    #     db.commit()
    #     db.refresh(user)

    #     return user
    def create_user(self, user_data: UserCreate):
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        return self.user_repo.create(user)
    
    #update a user
    def update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
    ):
        user = self.user_repo.get_by_id(user_id)

        if not user:
            return None
        update_data = user_data.model_dump(
            exclude_unset=True
        )
        
        for field, value in update_data.items():
            setattr(user, field, value)

        return self.user_repo.update(user)
    
    #soft-delete a user
    def delete_user(self, user_id: int):

        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None

        return self.user_repo.soft_delete(user)
    
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.orm import Session
from src.api.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db
        
    #get all users
    def get_all(self):
        result = self.db.execute(
            select(User)
            .where(User.deleted_at.is_(None))
            .order_by(User.id)
        )

        return result.scalars().all()
    
    #get a user by id
    def get_by_id(self, user_id: int):
        return self.db.execute(
            select(User)
            .where(
                User.id == user_id,
                User.deleted_at.is_(None),
            )
        ).scalar_one_or_none()

    #get user by email
    def get_by_email(self, email: str):
        return self.db.execute(
            select(User)
            .where(
                User.email == email,
                User.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        
    #create a new user
    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    #update a user
    def update(self, user: User):
        self.db.commit()
        self.db.refresh(user)

        return user
    
    #soft delete a user
    def soft_delete(self, user: User):

        user.deleted_at = datetime.utcnow()
        user.is_active = False

        self.db.commit()
        self.db.refresh(user)

        return user
from fastapi import APIRouter,Depends
from src.api.schemas.user import (UserCreate, UserUpdate, UserResponse)
from sqlalchemy.orm import Session
from src.api.database.database import get_db
from src.api.models.user import User
from src.api.security.dependencies import get_current_user
from src.api.controller.user_controller import UserController

router = APIRouter()

#get all users
@router.get("/",response_model=list[UserResponse],)
async def get_users(
    db: Session = Depends(get_db),
):
    return UserController.get_users(db)

#get current user
@router.get("/me",response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),db: Session = Depends(get_db),
):
    return UserController.get_me(
        db,
        current_user.id,
    )

#get user by id
@router.get("/{user_id}",response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return UserController.get_user(
        db,
        user_id,
    )

#create a new user by admin or user with role
@router.post("/",response_model=UserResponse)
async def create_user(
    request: UserCreate,
    db: Session = Depends(get_db),
):
    return UserController.create_user(
        db,
        request,
    )

#update current user profile
@router.put("/me",response_model=UserResponse,)
async def update_my_profile(
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserController.update_user(
        db,
        current_user.id,
        request,
    )


@router.delete("/{user_id}",response_model=UserResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return UserController.delete_user(
        db,
        user_id,
    )
    
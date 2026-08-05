from fastapi import APIRouter,status
from src.api.schemas.user import UserCreate, UserUpdate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from src.api.database.database import get_db
from src.api.services.user_service import UserService

router = APIRouter()
users = []  # In-memory storage for users

@router.get("/",response_model=list[UserResponse])
async def get_users(status_code: int = status.HTTP_200_OK,db: Session = Depends(get_db)):
    return UserService.get_users(db)
    # if not users:
    #     return {
    #         "response": {
    #             "status": status.HTTP_404_NOT_FOUND,
    #             "users": [],
    #             "data": {
    #                 "message": "No users found",
    #                 "error": "No users available in the system"
    #             }
    #         }
    #     }
    # return {
    #     "response": {
    #         "status": status_code,
    #         "content": [user.__dict__ for user in users],
    #         "data": {
    #             "message": "Users retrieved successfully",
    #             "error": None
    #         }
    #     }
    # }
    
# @router.get("/{id}")
# async def get_user(id: int, status_code: int = status.HTTP_200_OK):
#     user = next((user for user in users if user.id == id), None)
#     if not user:
#         return {
#             "response": {
#                 "status": status.HTTP_404_NOT_FOUND,
#                 "user": None,
#                 "data": {
#                     "message": f"User with ID {id} not found",
#                     "error": "User does not exist"
#                 }
#             }
#         }
#     return {
#         "response": {
#             "status": status_code,
#             "content": user.__dict__,
#             "data": {
#                 "message": f"User with ID {id} retrieved successfully",
#                 "error": None
#             }
#         }
#     }

# @router.post("/")
# async def create_user(user: UserCreate, status_code: int = status.HTTP_201_CREATED):
#     if any(existing_user.email == user.email for existing_user in users):
#         return {
#             "response": {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "user": None,
#                 "data": {
#                     "message": f"User with email {user.email} already exists",
#                     "error": "Duplicate email"
#                 }
#             }
#         }
#     users.append(user)
    
#     return {
#         "response": {
#             "status": status_code,
#             "content": user.__dict__,
#             "data": {
#                 "message": f"User with email {user.email} created successfully",
#                 "error": None
#             }
#         }
#     }
    
# @router.put("/{id}")
# async def update_user(id: int, updated_user: UserUpdate, status_code: int = status.HTTP_200_OK):
#     user_index = next((index for index, user in enumerate(users) if user.id == id), None)
#     if user_index is None:
#         return {
#             "response": {
#                 "status": status.HTTP_404_NOT_FOUND,
#                 "user": None,
#                 "data": {
#                     "message": f"User with ID {id} not found",
#                     "error": "User does not exist"
#                 }
#             }
#         }
#     users[user_index] = updated_user
    
#     return {
#         "response": {
#             "status": status_code,
#             "content": updated_user.__dict__,
#             "data": {
#                 "message": f"User with ID {id} updated successfully",
#                 "error": None
#             }
#         }
#     }
    
# @router.delete("/{id}")
# async def delete_user(id: int, status_code: int = status.HTTP_200_OK):
#     user_index = next((index for index, user in enumerate(users) if user.id == id), None)
#     if user_index is None:
#         return {
#             "response": {
#                 "status": status.HTTP_404_NOT_FOUND,
#                 "user": None,
#                 "data": {
#                     "message": f"User with ID {id} not found",
#                     "error": "User does not exist"
#                 }
#             }
#         }
#     deleted_user = users.pop(user_index)
    
#     return {
#         "response": {
#             "status": status_code,
#             "content": deleted_user.__dict__,
#             "data": {
#                 "message": f"User with ID {id} deleted successfully",
#                 "error": None
#             }
#         }
#     }
                
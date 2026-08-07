from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.database.database import get_db
from src.api.controller.saved_lesson_controller import (
    get_saved_lessons,
    save_lesson,
    remove_saved_lesson,
)
from src.api.schemas.saved_lesson import (
    SavedLessonResponse,
)
from src.api.security.dependencies import (
    get_current_user,
)
from src.api.models.user import User


router = APIRouter()


@router.get(
    "/",
    response_model=list[SavedLessonResponse],
)
def list_saved_lessons(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_saved_lessons(
        current_user.id,
        db,
    )


@router.post(
    "/{lesson_day_id}",
    response_model=SavedLessonResponse,
)
def save_lesson_day(
    lesson_day_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return save_lesson(
        current_user.id,
        lesson_day_id,
        db,
    )


@router.delete(
    "/{lesson_day_id}",
)
def unsave_lesson_day(
    lesson_day_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return remove_saved_lesson(
        current_user.id,
        lesson_day_id,
        db,
    )
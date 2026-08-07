from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.database.database import get_db
from src.api.controller.lesson_controller import (
    get_lessons,
    get_lesson,
    get_lessons_by_quarter,
    create_lesson,
    update_lesson,
    delete_lesson,
    get_lesson_days,
    get_lesson_day,
    create_lesson_day,
    update_lesson_day,
    delete_lesson_day,
)

from src.api.schemas.lesson import (
    LessonCreate,
    LessonUpdate,
    LessonResponse,
    LessonDayCreate,
    LessonDayUpdate,
    LessonDayResponse,
)

from src.api.security.dependencies import (
    get_current_user,
)


router = APIRouter()

#Lesson routes
@router.get(
    "/",
    response_model=list[LessonResponse],
)
def list_lessons(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_lessons(db)


@router.get(
    "/quarter/{quarter_id}",
    response_model=list[LessonResponse],
)
def list_quarter_lessons(
    quarter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_lessons_by_quarter(
        quarter_id,
        db,
    )


@router.get(
    "/{lesson_id}",
    response_model=LessonResponse,
)
def retrieve_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_lesson(
        lesson_id,
        db,
    )


@router.post(
    "/",
    response_model=LessonResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_lesson(
    request: LessonCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_lesson(
        request,
        db,
    )


@router.patch(
    "/{lesson_id}",
    response_model=LessonResponse,
)
def modify_lesson(
    lesson_id: int,
    request: LessonUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_lesson(
        lesson_id,
        request,
        db,
    )


@router.delete(
    "/{lesson_id}",
)
def remove_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return delete_lesson(
        lesson_id,
        db,
    )


#lesson day routes
@router.get(
    "/{lesson_id}/days",
    response_model=list[LessonDayResponse],
)
def list_lesson_days(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_lesson_days(
        lesson_id,
        db,
    )


@router.get(
    "/days/{lesson_day_id}",
    response_model=LessonDayResponse,
)
def retrieve_lesson_day(
    lesson_day_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_lesson_day(
        lesson_day_id,
        db,
    )


@router.post(
    "/{lesson_id}/days",
    response_model=LessonDayResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_lesson_day(
    lesson_id: int,
    request: LessonDayCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_lesson_day(
        lesson_id,
        request,
        db,
    )


@router.patch(
    "/days/{lesson_day_id}",
    response_model=LessonDayResponse,
)
def modify_lesson_day(
    lesson_day_id: int,
    request: LessonDayUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_lesson_day(
        lesson_day_id,
        request,
        db,
    )


@router.delete(
    "/days/{lesson_day_id}",
)
def remove_lesson_day(
    lesson_day_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return delete_lesson_day(
        lesson_day_id,
        db,
    )
from sqlalchemy.orm import Session

from src.api.services.saved_lesson_service import (
    SavedLessonService,
)


def get_saved_lessons(
    user_id: int,
    db: Session,
):
    service = SavedLessonService(db)

    return service.get_saved_lessons(
        user_id
    )


def save_lesson(
    user_id: int,
    lesson_day_id: int,
    db: Session,
):
    service = SavedLessonService(db)

    return service.save_lesson(
        user_id,
        lesson_day_id,
    )


def remove_saved_lesson(
    user_id: int,
    lesson_day_id: int,
    db: Session,
):
    service = SavedLessonService(db)

    service.remove_saved_lesson(
        user_id,
        lesson_day_id,
    )

    return {
        "message": "Lesson removed from saved lessons"
    }
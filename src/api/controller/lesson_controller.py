from sqlalchemy.orm import Session

from src.api.services.lesson_service import (
    LessonService,
)


def get_lessons(db: Session):
    service = LessonService(db)

    return service.get_lessons()


def get_lesson(
    lesson_id: int,
    db: Session,
):
    service = LessonService(db)

    return service.get_lesson(
        lesson_id
    )


def get_lessons_by_quarter(
    quarter_id: int,
    db: Session,
):
    service = LessonService(db)

    return service.get_lessons_by_quarter(
        quarter_id
    )


def create_lesson(
    request,
    db: Session,
):
    service = LessonService(db)

    return service.create_lesson(
        request
    )


def update_lesson(
    lesson_id: int,
    request,
    db: Session,
):
    service = LessonService(db)

    return service.update_lesson(
        lesson_id,
        request,
    )


def delete_lesson(
    lesson_id: int,
    db: Session,
):
    service = LessonService(db)

    service.delete_lesson(
        lesson_id
    )

    return {
        "message": "Lesson deleted successfully"
    }

#Lesson Day CRUD operations
def get_lesson_days(
    lesson_id: int,
    db: Session,
):
    service = LessonService(db)

    return service.get_lesson_days(
        lesson_id
    )


def get_lesson_day(
    lesson_day_id: int,
    db: Session,
):
    service = LessonService(db)

    return service.get_lesson_day(
        lesson_day_id
    )


def create_lesson_day(
    lesson_id: int,
    request,
    db: Session,
):
    service = LessonService(db)

    return service.create_lesson_day(
        lesson_id,
        request,
    )


def update_lesson_day(
    lesson_day_id: int,
    request,
    db: Session,
):
    service = LessonService(db)

    return service.update_lesson_day(
        lesson_day_id,
        request,
    )


def delete_lesson_day(
    lesson_day_id: int,
    db: Session,
):
    service = LessonService(db)

    service.delete_lesson_day(
        lesson_day_id
    )

    return {
        "message": "Lesson day deleted successfully"
    }
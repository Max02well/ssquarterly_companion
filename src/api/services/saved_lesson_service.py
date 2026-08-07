from fastapi import HTTPException, status

from src.api.models.saved_lesson import SavedLesson
from src.api.repository.saved_lesson_repository import SavedLessonRepository
from src.api.repository.lesson_repository import (
    LessonRepository,
)


class SavedLessonService:

    def __init__(self, db):
        self.repository = SavedLessonRepository(db)
        self.lesson_repository = LessonRepository(db)

    def get_saved_lessons(
        self,
        user_id: int,
    ):
        return self.repository.get_all_for_user(
            user_id
        )

    def save_lesson(
        self,
        user_id: int,
        lesson_day_id: int,
    ):

        lesson_day = (
            self.lesson_repository.get_day_by_id(
                lesson_day_id
            )
        )

        if not lesson_day:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson day not found",
            )

        existing = (
            self.repository.get_by_user_and_day(
                user_id,
                lesson_day_id,
            )
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Lesson already saved",
            )

        saved = SavedLesson(
            user_id=user_id,
            lesson_day_id=lesson_day_id,
        )

        return self.repository.create(
            saved
        )

    def remove_saved_lesson(
        self,
        user_id: int,
        lesson_day_id: int,
    ):

        saved = (
            self.repository.get_by_user_and_day(
                user_id,
                lesson_day_id,
            )
        )

        if not saved:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Saved lesson not found",
            )

        return self.repository.delete(
            saved
        )
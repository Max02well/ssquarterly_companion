from fastapi import HTTPException, status

from src.api.models.lesson import Lesson
from src.api.models.lesson_day import LessonDay

from src.api.repository.lesson_repository import (
    LessonRepository,
)


class LessonService:

    def __init__(self, db):
        self.repository = LessonRepository(db)

    #Lesson CRUD operations
    def get_lessons(self):
        return self.repository.get_all()

    def get_lesson(self, lesson_id: int):

        lesson = self.repository.get_by_id(
            lesson_id
        )

        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found",
            )

        return lesson

    def get_lessons_by_quarter(
        self,
        quarter_id: int,
    ):
        return self.repository.get_by_quarter(
            quarter_id
        )

    def create_lesson(self, request):

        lesson = Lesson(
            quarter_id=request.quarter_id,
            lesson_number=request.lesson_number,
            title=request.title,
            description=request.description,
        )

        return self.repository.create(lesson)

    def update_lesson(
        self,
        lesson_id: int,
        request,
    ):

        lesson = self.get_lesson(
            lesson_id
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                lesson,
                field,
                value,
            )

        return self.repository.update(
            lesson
        )

    def delete_lesson(
        self,
        lesson_id: int,
    ):

        lesson = self.get_lesson(
            lesson_id
        )

        return self.repository.delete(
            lesson
        )

    #Lesson Day CRUD operations
    def get_lesson_days(
        self,
        lesson_id: int,
    ):

        self.get_lesson(lesson_id)

        return self.repository.get_days(
            lesson_id
        )

    def get_lesson_day(
        self,
        lesson_day_id: int,
    ):

        lesson_day = (
            self.repository.get_day_by_id(
                lesson_day_id
            )
        )

        if not lesson_day:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson day not found",
            )

        return lesson_day

    def create_lesson_day(
        self,
        lesson_id: int,
        request,
    ):

        self.get_lesson(lesson_id)

        lesson_day = LessonDay(
            lesson_id=lesson_id,
            day_number=request.day_number,
            date=request.date,
            title=request.title,
            content=request.content,
            scripture_references=(
                request.scripture_references
            ),
        )

        return self.repository.create_day(
            lesson_day
        )

    def update_lesson_day(
        self,
        lesson_day_id: int,
        request,
    ):

        lesson_day = self.get_lesson_day(
            lesson_day_id
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                lesson_day,
                field,
                value,
            )

        return self.repository.update_day(
            lesson_day
        )

    def delete_lesson_day(
        self,
        lesson_day_id: int,
    ):

        lesson_day = self.get_lesson_day(
            lesson_day_id
        )

        return self.repository.delete_day(
            lesson_day
        )
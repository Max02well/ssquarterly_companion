from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.models.lesson import Lesson
from src.api.models.lesson_day import LessonDay


class LessonRepository:

    def __init__(self, db: Session):
        self.db = db

    #Lesson CRUD operations
    def get_all(self):
        result = self.db.execute(
            select(Lesson)
            .order_by(
                Lesson.quarter_id,
                Lesson.lesson_number,
            )
        )

        return result.scalars().all()

    def get_by_id(self, lesson_id: int):
        return self.db.get(
            Lesson,
            lesson_id,
        )

    def get_by_quarter(
        self,
        quarter_id: int,
    ):
        result = self.db.execute(
            select(Lesson)
            .where(
                Lesson.quarter_id == quarter_id
            )
            .order_by(
                Lesson.lesson_number
            )
        )

        return result.scalars().all()

    def create(self, lesson: Lesson):
        self.db.add(lesson)
        self.db.commit()
        self.db.refresh(lesson)

        return lesson

    def update(self, lesson: Lesson):
        self.db.commit()
        self.db.refresh(lesson)

        return lesson

    def delete(self, lesson: Lesson):
        self.db.delete(lesson)
        self.db.commit()

        return lesson

    #Lesson Day CRUD operations
    # def get_day_by_lesson_and_number(
    #     self,
    #     lesson_id: int,
    #     day_number: int,
    # ):
    #     result = self.db.execute(
    #         select(LessonDay)
    #         .where(
    #             LessonDay.lesson_id == lesson_id,
    #             LessonDay.day_number == day_number,
    #         )
    #     )

    #     return result.scalar_one_or_none()
    
    
    def get_day_by_id(
        self,
        lesson_day_id: int,
    ):
        return self.db.get(
            LessonDay,
            lesson_day_id,
        )

    def get_days(
        self,
        lesson_id: int,
    ):
        result = self.db.execute(
            select(LessonDay)
            .where(
                LessonDay.lesson_id == lesson_id
            )
            .order_by(
                LessonDay.day_number
            )
        )

        return result.scalars().all()

    def create_day(
        self,
        lesson_day: LessonDay,
    ):
        self.db.add(lesson_day)
        self.db.commit()
        self.db.refresh(lesson_day)

        return lesson_day

    def update_day(
        self,
        lesson_day: LessonDay,
    ):
        self.db.commit()
        self.db.refresh(lesson_day)

        return lesson_day

    def delete_day(
        self,
        lesson_day: LessonDay,
    ):
        self.db.delete(lesson_day)
        self.db.commit()

        return lesson_day
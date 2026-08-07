from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.models.saved_lesson import SavedLesson


class SavedLessonRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(
        self,
        user_id: int,
    ):
        result = self.db.execute(
            select(SavedLesson)
            .where(
                SavedLesson.user_id == user_id
            )
            .order_by(
                SavedLesson.created_at.desc()
            )
        )

        return result.scalars().all()

    def get_by_id(
        self,
        saved_lesson_id: int,
    ):
        return self.db.get(
            SavedLesson,
            saved_lesson_id,
        )

    def get_by_user_and_day(
        self,
        user_id: int,
        lesson_day_id: int,
    ):
        result = self.db.execute(
            select(SavedLesson)
            .where(
                SavedLesson.user_id == user_id,
                SavedLesson.lesson_day_id
                == lesson_day_id,
            )
        )

        return result.scalar_one_or_none()

    def create(
        self,
        saved_lesson: SavedLesson,
    ):
        self.db.add(saved_lesson)
        self.db.commit()
        self.db.refresh(saved_lesson)

        return saved_lesson

    def delete(
        self,
        saved_lesson: SavedLesson,
    ):
        self.db.delete(saved_lesson)
        self.db.commit()

        return saved_lesson
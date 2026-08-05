from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.base import Base


class SavedLesson(Base):

    __tablename__ = "saved_lessons"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "lesson_day_id",
            name="uq_user_saved_lesson",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    lesson_day_id: Mapped[int] = mapped_column(
        ForeignKey("lesson_days.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="saved_lessons",
    )

    lesson_day = relationship(
        "LessonDay",
        back_populates="saved_by_users",
    )
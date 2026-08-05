from datetime import date as DateType, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.base import Base


class LessonDay(Base):

    __tablename__ = "lesson_days"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    day_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    date: Mapped[DateType | None] = mapped_column(
        Date,
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    scripture_references: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    lesson = relationship(
        "Lesson",
        back_populates="days",
    )

    saved_by_users = relationship(
        "SavedLesson",
        back_populates="lesson_day",
        cascade="all, delete-orphan",
    )

    conversations = relationship(
        "ChatConversation",
        back_populates="lesson_day",
    )

    generated_audio = relationship(
        "GeneratedAudio",
        back_populates="lesson_day",
    )
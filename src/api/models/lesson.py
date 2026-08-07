from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.base import Base


class Lesson(Base):

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    quarter_id: Mapped[int] = mapped_column(
        ForeignKey("quarters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    lesson_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
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

    quarter = relationship(
        "Quarterly",
        back_populates="lessons",
    )

    days = relationship(
        "LessonDay",
        back_populates="lesson",
        cascade="all, delete-orphan",
        order_by="LessonDay.day_number",
        lazy="selectin",
    )
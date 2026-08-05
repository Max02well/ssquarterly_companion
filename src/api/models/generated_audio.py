from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.base import Base
from src.api.models.enums import AudioStatus


class GeneratedAudio(Base):

    __tablename__ = "generated_audio"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    lesson_day_id: Mapped[int | None] = mapped_column(
        ForeignKey("lesson_days.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    status: Mapped[AudioStatus] = mapped_column(
        Enum(AudioStatus),
        default=AudioStatus.PENDING,
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    script: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    audio_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="generated_audio",
    )

    lesson_day = relationship(
        "LessonDay",
        back_populates="generated_audio",
    )
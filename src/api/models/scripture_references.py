import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    Enum,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from src.api.database.base import Base


class ScriptureReference(Base):

    __tablename__ = "scripture_references"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    lesson_day_id: Mapped[int] = mapped_column(
        ForeignKey("lesson_days.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    book: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    chapter: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_verse: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    end_verse: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    translation: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    reference_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
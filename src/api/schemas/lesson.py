from datetime import date as Date, datetime

from pydantic import BaseModel, ConfigDict


#Scripture Reference Schemas
class ScriptureReferenceBase(BaseModel):
    book: str
    chapter: int
    start_verse: int | None = None
    end_verse: int | None = None
    translation: str | None = None
    reference_text: str | None = None
    
class ScriptureReferenceCreate(
    ScriptureReferenceBase
):
    pass

class ScriptureReferenceUpdate(BaseModel):
    book: str | None = None
    chapter: int | None = None
    start_verse: int | None = None
    end_verse: int | None = None
    translation: str | None = None
    reference_text: str | None = None


class ScriptureReferenceResponse(
    ScriptureReferenceBase
):
    id: int
    lesson_day_id: int

    model_config = ConfigDict(
        from_attributes=True
    )


#Lesson Day Schemas
class LessonDayCreate(BaseModel):
    day_number: int
    date: Date | None = None
    title: str
    content: str | None = None
    scripture_references: str | None = None


class LessonDayUpdate(BaseModel):
    day_number: int | None = None
    date: Date | None = None
    title: str | None = None
    content: str | None = None
    scripture_references: str | None = None


class LessonDayResponse(BaseModel):
    id: int
    lesson_id: int
    day_number: int
    date: Date | None
    title: str
    content: str | None
    scripture_references: str | None
    created_at: datetime
    updated_at: datetime

    scripture_references: list[
        ScriptureReferenceResponse
    ] = []

    model_config = ConfigDict(
        from_attributes=True
    )


#Lesson Schemas
class LessonCreate(BaseModel):
    quarter_id: int
    lesson_number: int
    title: str
    description: str | None = None


class LessonUpdate(BaseModel):
    quarter_id: int | None = None
    lesson_number: int | None = None
    title: str | None = None
    description: str | None = None


class LessonResponse(BaseModel):
    id: int
    quarter_id: int
    lesson_number: int
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class LessonDetailResponse(
    LessonResponse
):
    days: list[LessonDayResponse] = []
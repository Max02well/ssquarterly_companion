from datetime import datetime

from pydantic import BaseModel


class SavedLessonCreate(BaseModel):
    lesson_day_id: int


class SavedLessonResponse(BaseModel):
    id: int
    lesson_day_id: int
    created_at: datetime
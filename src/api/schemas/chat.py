
from datetime import datetime

from pydantic import BaseModel


class CreateConversationRequest(BaseModel):
    lesson_day_id: int | None = None
    title: str | None = None


class SendMessageRequest(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


class ChatConversationResponse(BaseModel):
    id: int
    title: str | None
    lesson_day_id: int | None
    created_at: datetime
    messages: list[ChatMessageResponse] = []
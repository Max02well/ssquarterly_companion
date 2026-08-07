
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateConversationRequest(BaseModel):
    lesson_day_id: int | None = None
    title: str | None = None
    
class UpdateConversationRequest(BaseModel):
    title: str | None = None


class SendMessageRequest(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ChatConversationResponse(BaseModel):
    id: int
    title: str | None
    lesson_day_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ChatConversationDetailResponse(
    ChatConversationResponse
):
    messages: list[ChatMessageResponse] = []


class ChatResponse(BaseModel):
    conversation_id: int
    message: ChatMessageResponse
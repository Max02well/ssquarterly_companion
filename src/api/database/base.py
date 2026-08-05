from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# Import all models here to ensure they are registered with Base
from src.api.models.user import User
from src.api.models.refresh_token import RefreshToken
from src.api.models.lesson_day import LessonDay
from src.api.models.lesson import Lesson
from src.api.models.quarterly import Quarterly
from src.api.models.saved_lesson import SavedLesson
from src.api.models.generated_audio import GeneratedAudio
from src.api.models.chat_conversation import ChatConversation
from src.api.models.chat_message import ChatMessage
from src.api.models.enums import AudioStatus
from src.api.models.scripture_references import ScriptureReference

__all__ = ["User"," RefreshToken", "LessonDay", "Lesson", "Quarterly", "SavedLesson", "GeneratedAudio", "ChatConversation", "ChatMessage", "AudioStatus", "ScriptureReference"]  
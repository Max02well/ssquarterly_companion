from datetime import datetime

from pydantic import BaseModel


class GenerateAudioRequest(BaseModel):

    lesson_day_id: int

    voice: str | None = None

    podcast: bool = False


class AudioResponse(BaseModel):

    id: int

    lesson_day_id: int | None

    status: str

    title: str | None

    audio_url: str | None

    duration_seconds: int | None

    created_at: datetime
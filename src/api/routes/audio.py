from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from pydantic import BaseModel
# Import your actual retrieval and generation modules
# from src.retrieval.rag_retriever import get_daily_context
# from src.services.script_generator import generate_script
# from src.services.tts_engine import generate_podcast_audio

router = APIRouter(prefix="/audio", tags=["Audio Devotional"])

class AudioGenerationRequest(BaseModel):
    year: int
    quarter: int
    lesson_num: int
    day_of_week: str  # e.g., "Tuesday"

@router.post("/generate")
async def get_daily_podcast(payload: AudioGenerationRequest):
    try:
        # 1. Retrieve the Sabbath school text, Scripture, and matched EGW Commentary
        context = get_daily_context(
            year=payload.year, 
            quarter=payload.quarter, 
            lesson=payload.lesson_num, 
            day=payload.day_of_week
        )
        
        # 2. Build the cohesive text narrative script
        script_text = generate_script(
            quarterly=context["quarterly_text"],
            bible=context["bible_verses"],
            egw=context["egw_commentary"]
        )
        
        # 3. Process the text through the TTS engine to get the binary MP3 stream
        audio_data = await generate_podcast_audio(script_text)
        
        # 4. Stream the MP3 file directly back to the user
        return StreamingResponse(
            BytesIO(audio_data), 
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename=lesson_{payload.lesson_num}_{payload.day_of_week.lower()}.mp3"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio production pipeline failed: {str(e)}")
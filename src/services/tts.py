import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_podcast_audio(script_text: str) -> bytes:
    """
    Converts the generated markdown script into a natural-sounding MP3 file.
    """
    response = client.audio.speech.create(
        model="tts-1-hd",     # Use tts-1-hd for premium quality audio
        voice="alloy",        # Deep, warm, and professional voice
        input=script_text
    )
    # Return the raw binary audio content
    return response.content
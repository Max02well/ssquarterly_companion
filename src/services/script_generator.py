from typing import Dict, Any

def compile_podcast_prompt(quarterly_text: str, bible_text: str, egw_text: str) -> str:
    return f"""
You are an expert biblical narrator and theologian producing a devotional podcast script.
Your task is to synthesize the following materials into a warm, engaging, and deep daily devotional episode.

[DAILY SABBATH SCHOOL LESSON CONTENT]
{quarterly_text}

[SUPPORTING BIBLE VERSES]
{bible_text}

[ELLEN G. WHITE COMMENTARY CONTEXT]
{egw_text}

Format the output strictly as a professional, ready-to-read podcast script for a single narrator. 
Use dynamic transitions like "Let's unpack that..." or "This brings us to an incredible insight from Ellen White..."
Do not include technical stage directions like [sound effects] or [music plays] in the spoken text.
Keep the tone reverent, conversational, and highly practical.
"""
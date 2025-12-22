# core/audio_pipeline.py
from openai import OpenAI
import tempfile


def generate_audio_overview(docs):
    """Takes document text, writes a script, and generates audio."""

    # 1. Prepare Text (Limit to 15k chars)
    full_text = " ".join([d.page_content for d in docs])[:15000]

    client = OpenAI()

    # 2. Generate Script
    script_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a podcast host. Summarize this text engagingly. Do not just list facts; tell a story. Keep it under 2 minutes."},
            {"role": "user", "content": full_text}
        ]
    )
    script = script_completion.choices[0].message.content

    # 3. Generate Audio
    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=script
    )

    # 4. Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        audio_response.stream_to_file(tmp_audio.name)
        return tmp_audio.name
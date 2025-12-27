"""
Text-to-Speech Module (basic)

Uses gTTS (Google Text-to-Speech) to generate an MP3 that can be played in Streamlit.
This is a lightweight approach for a local Streamlit app: the browser plays the audio.
"""

from __future__ import annotations

from io import BytesIO
from typing import Optional, Tuple

from gtts import gTTS


class TextToSpeech:
    """Basic TTS wrapper using gTTS."""

    def __init__(self, language: str = "en"):
        self.language = language

    def synthesize_mp3(self, text: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Convert text into MP3 bytes.

        Returns:
            (mp3_bytes, error): Exactly one is non-None.
        """
        text = (text or "").strip()
        if not text:
            return None, "Nothing to speak."

        try:
            buf = BytesIO()
            tts = gTTS(text=text, lang=self.language)
            tts.write_to_fp(buf)
            return buf.getvalue(), None
        except Exception as e:
            return None, f"TTS failed: {e}"



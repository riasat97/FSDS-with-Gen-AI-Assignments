"""
Speech-to-Text Module (basic)

This is a minimal implementation that supports uploading audio files (WAV/FLAC)
and transcribing them using SpeechRecognition's Google Web Speech API.

Notes:
- This is intended as a "basic" demo (no Google Cloud setup required).
- It requires internet access for the Google Web Speech API.
- Supported formats here: WAV/AIFF/FLAC. (MP3/M4A need ffmpeg conversion.)
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional, Tuple

import speech_recognition as sr


class SpeechToText:
    """Basic speech-to-text wrapper."""

    def __init__(self, language: str = "en-US"):
        self.language = language
        self.recognizer = sr.Recognizer()

    def transcribe_file_bytes(self, file_bytes: bytes, *, suffix: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Transcribe audio bytes by writing to a temporary file first.

        Args:
            file_bytes: Raw bytes from an uploaded file.
            suffix: File extension including dot, e.g. ".wav" or ".flac"

        Returns:
            (text, error): Exactly one is non-None.
        """
        suffix = suffix.lower()
        if suffix not in {".wav", ".flac", ".aiff", ".aif", ".aifc"}:
            return None, "Unsupported audio format. Please upload WAV or FLAC for this basic implementation."

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_bytes)
                tmp_path = Path(tmp.name)

            with sr.AudioFile(str(tmp_path)) as source:
                audio = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio, language=self.language)
            return text, None

        except sr.UnknownValueError:
            return None, "Could not understand the audio (speech was unclear)."
        except sr.RequestError as e:
            return None, f"Speech recognition request failed: {e}"
        except Exception as e:
            return None, f"Transcription failed: {e}"
        finally:
            try:
                if "tmp_path" in locals() and tmp_path.exists():
                    tmp_path.unlink(missing_ok=True)
            except Exception:
                pass



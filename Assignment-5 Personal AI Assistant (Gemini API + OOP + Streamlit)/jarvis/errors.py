"""
Error types for JARVIS.

We use these to separate:
- user-facing message (safe, short)
- technical details (logged)
"""

from __future__ import annotations


class JarvisError(Exception):
    """Base error with a user-facing message."""

    def __init__(self, user_message: str, *, technical_message: str | None = None):
        super().__init__(technical_message or user_message)
        self.user_message = user_message
        self.technical_message = technical_message or user_message


class GeminiQuotaExceededError(JarvisError):
    """Raised when Gemini returns quota/resource exhausted / 429."""


class GeminiRequestError(JarvisError):
    """Raised when Gemini request fails for other reasons."""



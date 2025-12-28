# Project Structure

## Directory Layout

```
.
├── .env                      # Environment variables (API keys)
├── app.py                    # Streamlit UI entrypoint
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview + run instructions
├── STRUCTURE.md              # This file
│
├── config/                   # Configuration package
│   ├── __init__.py
│   └── settings.py           # Loads .env + shared settings/constants
│
├── jarvis/                   # Core assistant package (OOP)
│   ├── __init__.py
│   ├── assistant.py          # Orchestrates prompt → Gemini → memory
│   ├── errors.py             # Custom error types (quota, request failures, etc.)
│   ├── gemini_engine.py      # Gemini API wrapper
│   ├── logger.py             # Logging setup (logs/jarvis.log)
│   ├── memory.py             # Persistent conversation memory (data/memory.json)
│   ├── prompt_controller.py  # Roles + prompt formatting
│   ├── speech_to_text.py     # Mic speech-to-text (basic)
│   └── text_to_speech.py     # Spoken reply (basic)
│
├── data/
│   └── memory.json           # Conversation history (auto-created/updated)
│
└── logs/
    └── jarvis.log            # Runtime logs (auto-created)
```

## Module Responsibilities (Quick Reference)

| Module | Responsibility |
|---|---|
| `app.py` | Streamlit UI: chat, roles, voice input, exports, and error display |
| `config/settings.py` | Loads `.env` + stores model/memory configuration |
| `jarvis/assistant.py` | Main orchestrator (history → prompt → model → save) |
| `jarvis/prompt_controller.py` | Role-based “system prompts” + prompt assembly |
| `jarvis/gemini_engine.py` | Gemini request/stream wrapper + error classification |
| `jarvis/memory.py` | JSON-backed conversation persistence |
| `jarvis/speech_to_text.py` | Speech-to-text for recorded mic audio |
| `jarvis/text_to_speech.py` | Text-to-speech for short spoken replies |
| `jarvis/logger.py` | Rotating file logging configuration |
| `jarvis/errors.py` | User-friendly errors with technical details for logs |

## High-Level Flow

1. User speaks or types in `app.py`.
2. (Voice only) audio → `SpeechToText` → transcribed text.
3. `JarvisAssistant` builds a role-based prompt using `PromptController` + recent `Memory`.
4. `GeminiEngine` calls Gemini and returns a response (or raises a classified error).
5. UI displays the response; optionally generates short spoken audio via `TextToSpeech`.
6. Conversation is appended to `data/memory.json`; logs go to `logs/jarvis.log`.

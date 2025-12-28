# JARVIS – Personal AI Assistant (Gemini + OOP + Streamlit)

A simple personal AI assistant built with **Streamlit** UI + an **OOP** backend that uses **Google Gemini** for responses, **conversation memory** for context, **microphone voice input** (speech-to-text), and **spoken replies** (text-to-speech).

---

## Features

### Chat (Text)
- **Chat input**: type a question in the Streamlit chat input.
- **Role-based behavior**: switch the assistant role from the sidebar:
  - `general` – helpful assistant
  - `tutor` – explains step-by-step
  - `coder` – programming-focused responses
  - `career` – career coaching style

### Voice Input (Mic → Speech-to-Text)
- **Record in browser** using Streamlit’s mic widget (`st.audio_input`).
- **Two-stage recording UX**:
  - record → stop → preview appears
  - click **Transcribe & Send** (or discard and record again)
- Speech-to-text uses **SpeechRecognition** (Google Web Speech API).

### Spoken Output (Short Text-to-Speech)
- Optional **spoken reply** using **gTTS** (MP3 played in the browser).
- Spoken reply is intentionally short:
  - **Max spoken words** slider controls how long the audio is.
- Note: browsers usually block autoplay, so you may need to click **Play**.

### “Voice mode” concise answers
- If your message came from **mic transcription**, JARVIS requests a **short 2–3 sentence summary** (so voice interactions don’t feel boring).
- Typed messages remain normal length.

### Conversation Memory (Persistent)
- Conversation is saved to: `data/memory.json`
- On startup, memory is loaded and reused for context.
- Sidebar tools:
  - **Clear Memory**
  - **Export Conversation** (JSON/TXT download)

### Error Handling + Logging (Quota, etc.)
- Clear user-facing errors for common Gemini failures (like **quota exceeded / 429**).
- Logs are written to: `logs/jarvis.log` (rotating file).
- The UI keeps the **last error** visible as a top banner until you clear it.

---

## Project Structure

### Key files
- `app.py`: Streamlit UI
- `config/settings.py`: loads environment variables and config
- `jarvis/assistant.py`: orchestrates prompt building, Gemini calls, and memory
- `jarvis/gemini_engine.py`: Gemini API wrapper + error classification (quota, request failures)
- `jarvis/prompt_controller.py`: role system prompts + prompt formatting
- `jarvis/memory.py`: JSON-backed conversation memory (`data/memory.json`)
- `jarvis/speech_to_text.py`: speech-to-text (basic)
- `jarvis/text_to_speech.py`: text-to-speech (basic)
- `jarvis/logger.py`: logging configuration
- `jarvis/errors.py`: app-level error types used for clean UI errors

---

## Requirements

### Python packages (installed via `requirements.txt`)
- `streamlit`
- `google-generativeai` *(deprecated upstream; still works, but shows a warning)*
- `python-dotenv`
- `SpeechRecognition`
- `gTTS`

### Internet access
- Gemini API calls require internet.
- Speech-to-text (SpeechRecognition Google Web Speech API) requires internet.
- gTTS requires internet.

---

## Setup

### 1) Create `.env`
Create a `.env` file in the project root (same folder as `app.py`) with:

```env
GEMINI_API_KEY=your_api_key_here
```

If `GEMINI_API_KEY` is missing, the app will fail to initialize.

### 2) Create or use a conda environment
You can use any environment name. Examples below use `pai`.

Create the environment (recommended if you don’t have one yet):

```powershell
conda create -n pai python=3.11 -y
```

Activate it:

```powershell
conda activate pai
```

Install/update dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

## Run

From the project directory:

```powershell
conda activate pai
streamlit run .\app.py
```

Open:
- `http://localhost:8501`

---

## Usage Tips

### Voice input
- Allow microphone permission in the browser.
- Record → stop → preview → **Transcribe & Send**.
- If you want another recording, use **Discard & Record Again**.

### Spoken output
- Toggle **Speak JARVIS reply (short)** in the sidebar.
- Adjust **Max spoken words** to keep it brief.

### Quota / limit exceeded
If your Gemini quota is exhausted you’ll see a banner like “quota/rate limit reached”.
Details are also written to:
- `logs/jarvis.log`

---

## Known Limitations

### Gemini client library warning
`google-generativeai` is deprecated upstream, so you may see a warning at startup.
This repo currently keeps it for simplicity; migrating to `google-genai` is a good next improvement.

### Audio format support
- Mic recording produces WAV bytes (supported).
- If you later add file uploads: MP3/M4A typically require conversion (ffmpeg).

### Browser autoplay
Most browsers require a user gesture to play audio, so you may need to click play.



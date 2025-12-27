# JARVIS Project Structure

## Directory Layout

```
Assignment-5 Personal AI Assistant/
├── .env                          # Environment variables (API keys)
├── requirements.txt              # Python dependencies
├── app.py                        # Main Streamlit app
│
├── jarvis/                       # Main JARVIS package
│   ├── __init__.py              # Package initialization
│   ├── gemini_engine.py         # Gemini API communication
│   ├── prompt_controller.py     # Role-based prompts
│   ├── memory.py                # Conversation memory
│   └── assistant.py             # Main JARVIS class
│
├── config/                       # Configuration package
│   ├── __init__.py              # Package initialization
│   └── settings.py              # Settings and env management
│
└── data/                         # Data storage
    └── (conversation history, memory files)
```

## File Descriptions

| File | Purpose |
|------|---------|
| `config/settings.py` | Load and manage API keys, model settings, and constants |
| `jarvis/gemini_engine.py` | Handle Gemini API calls and responses |
| `jarvis/prompt_controller.py` | Manage different assistant roles (Tutor, Coder, etc.) |
| `jarvis/memory.py` | Save/load conversation history |
| `jarvis/assistant.py` | Orchestrate all components into main JARVIS assistant |
| `app.py` | Streamlit web interface |

## Build Order (Step by Step)

1. **config/settings.py** - Load environment variables
2. **jarvis/gemini_engine.py** - Set up API communication
3. **jarvis/prompt_controller.py** - Create role-based behaviors
4. **jarvis/memory.py** - Implement conversation memory
5. **jarvis/assistant.py** - Combine all components
6. **app.py** - Build web interface

## Next Steps

Ready to start building? Let's begin with **Step 1: config/settings.py**

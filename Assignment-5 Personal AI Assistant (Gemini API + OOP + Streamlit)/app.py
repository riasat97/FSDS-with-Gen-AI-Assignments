"""
JARVIS Personal AI Assistant - Streamlit UI
Main interface for the JARVIS assistant
"""

import streamlit as st
from jarvis.assistant import JarvisAssistant
from jarvis.prompt_controller import AssistantRole
from jarvis.speech_to_text import SpeechToText
from jarvis.text_to_speech import TextToSpeech
from jarvis.errors import JarvisError
from jarvis.logger import get_logger

logger = get_logger("app")


# Page configuration
st.set_page_config(
    page_title="JARVIS - Personal AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .user-message {
        background-color: #f0f0f0;
        color: #000000;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border: 2px solid #333333;
        font-size: 1.1em;
    }
    .assistant-message {
        background-color: #ffffff;
        color: #000000;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border: 2px solid #000000;
        font-size: 1.1em;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state (only once per session)
if "jarvis" not in st.session_state:
    try:
        st.session_state.jarvis = JarvisAssistant()
        st.session_state.init_success = True
    except Exception as e:
        st.session_state.jarvis = None
        st.session_state.init_success = False
        st.session_state.error_msg = str(e)

if "chat_history_display" not in st.session_state:
    st.session_state.chat_history_display = []

if "pending_user_input" not in st.session_state:
    st.session_state.pending_user_input = None

if "pending_user_input_source" not in st.session_state:
    st.session_state.pending_user_input_source = None

if "stt" not in st.session_state:
    st.session_state.stt = SpeechToText(language="en-US")

if "tts" not in st.session_state:
    st.session_state.tts = TextToSpeech(language="en")

if "mic_widget_version" not in st.session_state:
    # We bump this after each successful "Transcribe & Send" to force the mic widget to remount.
    # This avoids the "An error has occurred, please try" issue that can appear on repeated recordings.
    st.session_state.mic_widget_version = 0

if "mic_audio_bytes" not in st.session_state:
    st.session_state.mic_audio_bytes = None

if "last_app_error_message" not in st.session_state:
    st.session_state.last_app_error_message = None

if "last_app_error_details" not in st.session_state:
    st.session_state.last_app_error_details = None

if "last_tts_mp3" not in st.session_state:
    st.session_state.last_tts_mp3 = None

if "last_tts_for_index" not in st.session_state:
    st.session_state.last_tts_for_index = None

if "last_tts_error" not in st.session_state:
    st.session_state.last_tts_error = None


def _shorten_for_speech(text: str, max_words: int) -> str:
    words = (text or "").strip().split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]).rstrip() + "…"

# Check if initialization failed
if not st.session_state.init_success:
    st.error("❌ Failed to initialize JARVIS")
    st.error(f"Error: {st.session_state.error_msg}")
    st.info("Please check your API key in .env file and restart the app.")
    st.stop()

# Persistent error banner (always visible at top)
if st.session_state.get("last_app_error_message"):
    logger.warning("Displaying persistent UI error banner: %s", st.session_state.last_app_error_message)
    st.error(st.session_state.last_app_error_message)
    with st.expander("Technical details (for debugging)", expanded=False):
        st.code(st.session_state.get("last_app_error_details") or "")
    if st.button("Clear error", key="clear_last_error"):
        st.session_state.last_app_error_message = None
        st.session_state.last_app_error_details = None
        st.rerun()

# Main title
st.markdown("<h1 class='main-title'>🧠 JARVIS – Your AI Assistant</h1>", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Role Selection
    st.subheader("Assistant Role")
    roles = st.session_state.jarvis.get_available_roles()
    selected_role = st.selectbox(
        "Choose your assistant's role:",
        options=list(roles.keys()),
        format_func=lambda x: roles[x],
        key="role_selector"
    )
    
    if selected_role:
        role = AssistantRole(selected_role)
        message = st.session_state.jarvis.set_role(role)
        st.success(f"✓ {message}")
    
    st.divider()
    
    # Memory Management
    st.subheader("💾 Memory Management")
    memory_summary = st.session_state.jarvis.get_memory_summary()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Messages", memory_summary["total_messages"])
    with col2:
        st.metric("User Messages", memory_summary["user_messages"])
    
    st.metric("Assistant Messages", memory_summary["assistant_messages"])
    
    if st.button("🗑️ Clear Memory", key="clear_memory"):
        result = st.session_state.jarvis.clear_memory()
        st.success(result)
        st.rerun()
    
    st.divider()
    
    # Export Conversation
    st.subheader("📥 Export Conversation")
    export_format = st.radio("Export as:", ["JSON", "TXT"], key="export_format")
    
    if st.button("⬇️ Download Conversation", key="export_conversation"):
        format_map = {"JSON": "json", "TXT": "txt"}
        export_data = st.session_state.jarvis.export_conversation(format_map[export_format])
        file_ext = "json" if export_format == "JSON" else "txt"
        st.download_button(
            label=f"Save as {file_ext.upper()}",
            data=export_data,
            file_name=f"jarvis_conversation.{file_ext}",
            mime="application/json" if export_format == "JSON" else "text/plain"
        )
    
    st.divider()

    # Voice Input (Mic) + Spoken Output
    st.subheader("🎤 Voice Input (Mic)")
    st.caption("Record your voice in the browser → it will be transcribed and sent as your next message.")

    speak_reply = st.checkbox("🔊 Speak JARVIS reply (short)", value=True, key="speak_reply")
    max_spoken_words = st.slider("Max spoken words", min_value=10, max_value=120, value=45, step=5, key="max_spoken_words")

    # Two-stage flow:
    # 1) Record in-browser (audio_input)
    # 2) Show captured preview + actions (transcribe / discard)
    #
    # This avoids the recorder showing an error state after stopping, by rerendering
    # into a "captured" view as soon as the bytes are available.
    if st.session_state.mic_audio_bytes is None:
        mic_key = f"audio_input_{st.session_state.mic_widget_version}"
        audio_recording = st.audio_input("Record a voice message", key=mic_key)

        if audio_recording is not None:
            audio_bytes = (
                audio_recording.getvalue() if hasattr(audio_recording, "getvalue") else audio_recording.read()
            )
            st.session_state.mic_audio_bytes = audio_bytes
            # Prepare next recording key now (even if user discards/records again).
            st.session_state.mic_widget_version += 1
            st.rerun()
    else:
        st.caption("Captured audio:")
        st.audio(st.session_state.mic_audio_bytes, format="audio/wav")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📝 Transcribe & Send", key="transcribe_and_send"):
                with st.spinner("Transcribing..."):
                    text, err = st.session_state.stt.transcribe_file_bytes(st.session_state.mic_audio_bytes, suffix=".wav")
                    if err:
                        st.error(err)
                    else:
                        st.session_state.pending_user_input = text
                        st.session_state.pending_user_input_source = "voice"
                        st.session_state.mic_audio_bytes = None
                        st.success(f"Transcribed: {text}")
                        st.rerun()
        with col_b:
            if st.button("🗑️ Discard & Record Again", key="discard_audio"):
                st.session_state.mic_audio_bytes = None
                st.rerun()
    
    st.subheader("ℹ️ About")
    st.info(
        "JARVIS is your personal AI assistant powered by Google Gemini. "
        "Switch between different roles (Tutor, Coder, Career) to get specialized responses."
    )

# Main chat interface
st.subheader("💬 New Message")
user_input = st.chat_input("Ask JARVIS...")

pending_input = user_input or st.session_state.pending_user_input
st.session_state.pending_user_input = None
pending_source = st.session_state.pending_user_input_source
st.session_state.pending_user_input_source = None

if pending_input:
    try:
        # Display user message immediately
        st.markdown(f"<div class='user-message'><b>👤 You:</b> {pending_input}</div>", unsafe_allow_html=True)
        
        # Normal mode - wait for full response
        with st.spinner("JARVIS is thinking..."):
            if pending_source == "voice":
                response = st.session_state.jarvis.respond(
                    pending_input,
                    prompt_hint="Reply as a short, clear summary in 2–3 sentences (max ~60 words). No long lists.",
                    store_user_input=pending_input,
                )
            else:
                response = st.session_state.jarvis.respond(pending_input)
            st.markdown(f"<div class='assistant-message'><b>🧠 JARVIS:</b> {response}</div>", unsafe_allow_html=True)
            # Clear any previous persistent error after a successful response
            st.session_state.last_app_error_message = None
            st.session_state.last_app_error_details = None

            if st.session_state.get("speak_reply", True):
                short_text = _shorten_for_speech(response, st.session_state.get("max_spoken_words", 45))
                mp3_bytes, err = st.session_state.tts.synthesize_mp3(short_text)
                # Persist across st.rerun() so the audio player is visible in Chat History.
                st.session_state.last_tts_mp3 = mp3_bytes
                st.session_state.last_tts_error = err
                st.session_state.last_tts_for_index = len(st.session_state.jarvis.get_conversation_history()) - 1
    
    except JarvisError as e:
        # Show clear, user-facing error (quota exceeded, etc.)
        st.session_state.last_app_error_message = e.user_message
        st.session_state.last_app_error_details = e.technical_message
        logger.warning("JarvisError shown to user: %s", e.user_message)
        st.error(e.user_message)
        with st.expander("Technical details (for debugging)"):
            st.code(e.technical_message)
        # Stop the run so the error stays visible in-place (no disappearing due to rerun).
        st.stop()

    except Exception as e:
        st.session_state.last_app_error_message = "❌ Unexpected error. Please try again."
        st.session_state.last_app_error_details = str(e)
        logger.exception("Unexpected error in app")
        st.error(st.session_state.last_app_error_message)
        with st.expander("Technical details (for debugging)"):
            st.code(st.session_state.last_app_error_details)
        st.stop()

st.divider()

# Display chat history below
st.subheader("💬 Chat History")

# Display chat history
conversation_history = st.session_state.jarvis.get_conversation_history()

if conversation_history:
    for idx, msg in enumerate(conversation_history):
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'><b>👤 You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'><b>🧠 JARVIS:</b> {msg['content']}</div>", unsafe_allow_html=True)
            if (
                st.session_state.get("last_tts_for_index") == idx
                and st.session_state.get("last_tts_mp3") is not None
            ):
                st.audio(st.session_state.last_tts_mp3, format="audio/mp3")
            elif st.session_state.get("last_tts_for_index") == idx and st.session_state.get("last_tts_error"):
                st.caption(f"TTS: {st.session_state.last_tts_error}")
else:
    st.info("No messages yet. Start a conversation!")

# JARVIS - AI Voice Assistant

JARVIS is an intelligent voice-controlled assistant powered by Google's Gemini AI. It can perform various tasks like opening websites, searching Wikipedia, telling time, and answering questions using natural language processing.

## Features

- **Voice Recognition**: Listens to user commands and converts speech to text using Google Speech Recognition
- **Text-to-Speech**: Speaks responses back to the user using pyttsx3
- **Web Browser Automation**: Opens YouTube, Google, and LinkedIn in new tabs using Selenium
- **Tab Management**: Close specific tabs (YouTube, LinkedIn, Wikipedia) or the entire browser
- **Wikipedia Search**: Search and retrieve information from Wikipedia
- **AI-Powered Responses**: Get concise answers to questions using Google Gemini API
- **Time Reporting**: Tells the current time on demand
- **Error Handling**: Comprehensive logging and error management
- **Environment Variable Support**: Secure API key management using .env file

## Requirements

- Python 3.11 or higher
- Google Gemini API Key
- Microphone for voice input
- Chrome/Chromium browser for web automation

## Installation

### 1. Create a Virtual Environment

```bash
conda create -n jarvis python=3.11 -y
```

### 2. Activate Virtual Environment

```bash
conda activate jarvis
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Google Gemini API key.

## How to Run

### Run the JARVIS Script

```bash
python jarvis.py
```

The program will greet you and start listening for commands.

## Folder Structure

```
Assignment-4/
├── jarvis.py              # Main JARVIS application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API key)
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
└── Logs/
    └── app.log            # Application logs
```

## Usage Commands

### Voice Commands

- **"What time is it?"** - Tells you the current time
- **"Wikipedia [topic]"** - Searches Wikipedia and reads the summary
- **"Open YouTube"** - Opens YouTube in the browser
- **"Open Google"** - Opens Google in the browser
- **"Open LinkedIn"** - Opens your LinkedIn profile
- **"Close YouTube"** - Closes the YouTube tab
- **"Close LinkedIn"** - Closes the LinkedIn tab
- **"Close Wikipedia"** - Closes the Wikipedia tab
- **"Close Chrome" / "Close Browser"** - Closes the entire browser
- **"Bye" / "Exit" / "Quit"** - Exits the application
- **[Any question]** - Asks Gemini AI and gets a concise answer

## Project Structure Explanation

### Main Components

1. **Speech Recognition** (`take_command()`)
   - Listens to microphone input
   - Converts speech to text using Google Speech Recognition API

2. **Text-to-Speech** (`speak()`)
   - Converts text responses to audio
   - Uses pyttsx3 engine with SAPI5

3. **Browser Automation** (`open_browser_tab()`, `close_specific_tab()`, `close_browser()`)
   - Manages Chrome browser using Selenium WebDriver
   - Opens new tabs if browser is already running
   - Detects if browser was manually closed and reinitializes

4. **Wikipedia Integration** (`wikipedia.summary()`)
   - Searches Wikipedia for topics
   - Retrieves and speaks the first 2 sentences

5. **AI Integration** (`ask_gemini()`)
   - Sends queries to Google Gemini API
   - Returns concise 2-3 sentence answers
   - Suitable for voice output

## Configuration Files

### `.env` File

Stores sensitive information like API keys:

```
GEMINI_API_KEY=your_api_key_here
```

### `requirements.txt`

Lists all Python dependencies required to run the application.

## Logging

All activities are logged in `Logs/app.log` with timestamps and log levels (INFO, WARNING, ERROR).

## Error Handling

- **Browser Crashes**: Automatically detects if browser is closed and creates a new instance
- **API Failures**: Graceful error handling for Gemini API calls
- **Speech Recognition Errors**: Prompts user to repeat if audio is not recognized
- **Missing API Key**: Warns user if GEMINI_API_KEY is not set

## Requirements

The application requires the following Python packages (see `requirements.txt`):

- `speech_recognition` - For voice input
- `pyttsx3` - For text-to-speech
- `wikipedia` - For Wikipedia search
- `google-generativeai` - For Gemini AI integration
- `selenium` - For browser automation
- `python-dotenv` - For environment variable management

## Author

**Riasat Raihan Noor**

## License

This project is part of FSDS (Full Stack Data Science) bootcamp assignments.

## Notes

- Ensure your microphone is working properly for voice input
- Keep the Chrome browser closed when starting the application
- The Gemini API key can be obtained from [Google AI Studio](https://makersuite.google.com/app/apikey)
- For security, never commit the `.env` file to version control

## Troubleshooting

### "Access is denied" error during pip install
- Run PowerShell as Administrator
- Or use: `python -m pip install -r requirements.txt`

### Microphone not detected
- Check if microphone is properly connected
- Verify microphone permissions in Windows Settings

### Chrome not opening
- Ensure Chrome browser is installed
- Check if ChromeDriver version matches Chrome version

### API Key not working
- Verify the API key in `.env` file
- Ensure GEMINI_API_KEY environment variable is set correctly
- Check if your API key has remaining quota

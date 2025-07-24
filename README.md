# JARVIS-AI: Iron Man-Inspired Voice Assistant

## Overview
JARVIS-AI is a powerful, modular, and extensible AI assistant inspired by Iron Man's JARVIS. It features voice interaction, real-time web search, automation, AI-powered chat, image generation, and a modern graphical user interface. The assistant is designed for Windows and leverages state-of-the-art AI models and APIs for natural conversation, automation, and creativity.

---

## Features
- **Voice Interaction**: Speech-to-text and text-to-speech for hands-free operation.
- **Modern GUI**: PyQt5-based, animated, and visually appealing interface.
- **Conversational AI**: Chatbot powered by LLMs (Groq, Cohere, etc.).
- **Real-Time Web Search**: Fetches up-to-date information using Google Custom Search.
- **Automation**: Open/close apps, play YouTube, search Google/YouTube, system commands, reminders, and more.
- **AI Image Generation**: Create images from prompts using HuggingFace Stable Diffusion.
- **Content Generation**: Write content, generate presentations, and more using LLMs.
- **Persistent Chat Logs**: Stores and displays chat history.
- **Customizable**: Environment-based configuration for API keys, voices, and more.

---

## File Structure & Key Components

```
JARVIS-AI/
├── Backend/
│   ├── assistant_core.py         # Main logic: routes user input to correct module (chat, automation, image, etc.)
│   ├── Automation.py             # Automation: open/close apps, web search, YouTube, reminders, system commands
│   ├── Chatbot.py                # Conversational AI using Groq LLM
│   ├── ImageGeneration.py        # AI image generation via HuggingFace API
│   ├── Model.py                  # Decision-making model (Cohere): classifies user intent
│   ├── RealtimeSearchEngine.py   # Real-time web search (Google Custom Search + LLM summarization)
│   ├── SpeechToText.py           # Voice input (speech recognition, translation)
│   ├── TextToSpeech.py           # Voice output (text-to-speech, Edge TTS)
│   └── __pycache__/
├── Frontend/
│   ├── GUI.py                    # PyQt5 GUI: chat, status, animations, user input
│   ├── audio/
│   │   └── start_sound.mp3       # Startup sound
│   ├── Files/                    # Runtime data (status, responses, chat, etc.)
│   │   ├── Database.data         # Chat history for GUI
│   │   ├── ImageGeneration.data  # Image generation triggers
│   │   ├── Mic.data              # Microphone status
│   │   ├── Responses.data        # Latest assistant response
│   │   └── Status.data           # Assistant status
│   ├── Graphics/
│   │   └── jarvis.gif            # Animated JARVIS avatar
│   └── __pycache__/
├── Data/
│   ├── ChatLog.json              # Persistent chat log (user/assistant turns)
│   ├── speech.mp3                # Example audio output
│   ├── Surface_generate_image_of_iron_man.*.jpg # Generated images
│   └── Voice.html                # Simple web-based speech recognition demo
├── Logs/
│   └── startup.log               # Startup and error logs
├── main.py                       # Main entry point (initializes and runs the assistant)
├── JARVIS_START.bat              # Windows batch script to launch the assistant with style
├── Requirements.txt              # Python dependencies
└── README.md                     # (You are here)
```

---

## Setup & Installation

### 1. Clone the Repository
```sh
git clone <repo-url>
cd JARVIS-AI
```

### 2. Install Python Dependencies
Make sure you have Python 3.8+ and pip installed.
```sh
pip install -r Requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory with the following keys (get API keys from respective providers):
```
Username=YourName
Assistantname=JARVIS
GroqAPIKey=your_groq_api_key
CohereAPIKey=your_cohere_api_key
HuggingFaceAPIKey=your_huggingface_api_key
Google_API_KEY=your_google_api_key
CSE_ID=your_google_cse_id
AssistantVoice=en-US-JennyNeural
InputLanguage=en-US
EmailAddress=your_email@example.com
EmailPassword=your_email_password
```

### 4. (Windows) Start the Assistant
Double-click `JARVIS_START.bat` or run:
```sh
./JARVIS_START.bat
```
This will:
- Show a styled ASCII-art welcome
- Play a startup sound
- Launch the main assistant (`main.py`)

### 5. (Manual) Start via Python
```sh
python main.py
```

---

## Usage
- **Voice Commands**: Speak to JARVIS for queries, automation, or creative tasks.
- **Text Input**: Use the GUI to type commands or questions.
- **Image Generation**: Ask for images (e.g., "generate image of iron man").
- **Automation**: Open/close apps, search, play YouTube, set reminders, etc.
- **Real-Time Search**: Ask for news, stock prices, or anything requiring up-to-date info.
- **Content Generation**: Request emails, presentations, or creative writing.

### Example Queries
- "What's the weather today?"
- "Open Chrome and search for AI news."
- "Generate image of a futuristic city."
- "Play Let Her Go on YouTube."
- "Write an email to my boss about the meeting."

---

## Dependencies
All dependencies are listed in `Requirements.txt`. Key packages:
- `PyQt5`, `pygame`, `speech_recognition`, `edge-tts`, `cohere`, `groq`, `requests`, `AppOpener`, `pywhatkit`, `pillow`, `bs4`, `mtranslate`, `selenium`, `fastapi`, `uvicorn`, `pydantic`, etc.

Install with:
```sh
pip install -r Requirements.txt
```

---

## Troubleshooting
- **Missing API Keys**: Ensure all required keys are in your `.env` file.
- **Speech Recognition Errors**: Install `PocketSphinx` for offline fallback, or check your microphone.
- **Module Not Found**: Run `pip install -r Requirements.txt` again.
- **Startup Issues**: Check `Logs/startup.log` for error details.
- **Internet Required**: Some features (real-time search, LLMs, image generation) require an active internet connection.

---

## Credits
- Developed by uday-studio
- Powered by OpenAI, Groq, Cohere, HuggingFace, Google, and open-source Python libraries.

---

## License
This project is for educational and personal use. For commercial use, please check the licenses of the underlying APIs and libraries. 
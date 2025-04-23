# 🧠 Voice-Activated-Virtual-Assistant
A voice-activated virtual assistant designed to perform tasks such as web browsing, playing music, fetching news, and responding to user questions using gemini-1.5-pro-001 model.
---

## 🚀 Features

- 🔊 **Wake Word Activation**: Starts listening after you say **"Jarvis"**.
- 🗣️ **Speech Recognition**: Converts your speech to text using Google's Speech API.
- 🧠 **AI-Powered Answers**: Uses **Google Gemini (Generative AI)** for smart replies.
- 🎧 **Play Music**: Plays songs using links from a customizable music library.
- 🌐 **Web Navigation**: Opens popular websites like Google, YouTube, Facebook, etc.
- 📰 **News Headlines**: Fetches real-time news from the **NewsAPI**.
- 🛡️ **Command Filtering**: Prevents execution of unsafe commands like shutdown or delete.

---








## 🔄 Resetting Your Environment (If `env/` is Deleted/Not present)

If you accidentally deleted your `env/` folder (your virtual environment) or not having in your system, you can easily recreate it:

### Step 1: Recreate the virtual environment
python -m venv env

### step2:
Activate the environment
#### On Windows:
env\Scripts\activate

#### On macOS/Linux:
source env/bin/activate

### Step 3: Reinstall all required packages
pip install -r requirements.txt


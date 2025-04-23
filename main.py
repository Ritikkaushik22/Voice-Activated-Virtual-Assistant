# Import necessary modules
import speech_recognition as sr  # For voice recognition
import webbrowser  # For opening URLs in the browser
import pyttsx3  # For text-to-speech conversion
import musicLibrary  # Custom module for music URLs (assumed to be a dictionary)
import requests  # For making HTTP requests (like fetching news)
import google.generativeai as genai  # For Google Gemini AI interaction
from dotenv import load_dotenv  # To load environment variables from a .env file
import os  # For accessing environment variables
import logging  # For logging messages instead of using print

# Load environment variables from .env file (for API keys, etc.)
load_dotenv()


# Configure logging to show informational messages
logging.basicConfig(level=logging.INFO)

recognizer = sr.Recognizer()  # Create an instance of the Recognizer class
engine = pyttsx3.init()  # Initialize the pyttsx3 engine for text-to-speech

# Get API keys from environment variables
newsApi = os.getenv("NEWS_API_KEY")
genai_api_key=os.getenv("GENAI_API_KEY")
# Warn if the required API keys are missing
if not newsApi or not genai_api_key:
    logging.warning("API keys missing from .env file!")

# Function to make the program speak
def speak(text):
    engine.say(text)  # Convert the text to speech
    engine.runAndWait()  # Run the speech engine

# Function to process AI queries using Google Gemini
def aiProcess(command):
    genai.configure(api_key=genai_api_key)
    model = genai.GenerativeModel("gemini-1.5-pro-001")
    # Function to process AI queries using Google Gemini
    response = model.generate_content(f"{command}. Reply concisely in one or two sentences.")
    return response.text

# Function to filter out unsafe commands (e.g., shutdown, delete)
def is_safe_command(cmd):
    risky_words = ["shutdown", "format", "delete", "kill", "restart"]
    return not any(word in cmd.lower() for word in risky_words)


def processCommand(c):

    c = c.lower()  # Normalize command to lowercase

    # Open common websites
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif c.lower().startswith("play"):
        song = c.lower().replace("play ", "").strip()
        logging.info(f"Requested song: {song}")
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)    
        else:
            speak("Sorry, I couldn't find that song.")

    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsApi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles[:5]:  # Limit to first 5 headlines
                    speak(article['title'])
            else:
                speak("No news found.")
        else:
            speak("Failed to fetch news.")
            logging.error(f"News API error: {r.status_code}")
    
    # Stop the assistant if the user says "stop jarvis"
    elif "stop jarvis" in c:
        speak("Shutting down. Goodbye!")
        exit()
    
    # For all other commands, process them with Gemini AI (if safe)
    else:
        if is_safe_command(c):
            output = aiProcess(c)
            speak(output)
        else:
            speak("Sorry, I can't perform that action.")


if __name__ == "__main__":
    speak("Initializing Jarvis...")  # When the program starts, it speaks "Initializing Jarvis..."
    
    while True:
        # The program continuously listens for audio input from the microphone
        
        r = sr.Recognizer()  # Create a new Recognizer object each time inside the loop

        try:
            with sr.Microphone() as source:  # Use the microphone as the source of audio input
                logging.info("Listening for wake word...")  # Print that it's listening for the wake word
                audio = r.listen(source, timeout=2, phrase_time_limit=1)  # Listen for up to 2 seconds of audio

            # Use Google's speech recognition API to convert the audio to text
            logging.info("Recognizing...")  # trying to recognize what was said
            word = r.recognize_google(audio)  
            if(word.lower()=="jarvis"):
                speak("Yes?")
                #Listen for command
                with sr.Microphone() as source:  
                    logging.info("Jarvis is active. Listening for command...")  # Print that it's listening for the command
                    audio = r.listen(source)
                    command = r.recognize_google(audio)  
                    logging.info(f"Command received: {command}")
                    processCommand(command)
        except Exception as e:
            print(e)  # If an error occurs (e.g., speech not recognized), print the error

import speech_recognition as sr
import pyttsx3
import wikipedia
import google.generativeai as genai
import os
from datetime import datetime
import webbrowser
import subprocess
import random
import logging

#Log Configuration
LOG_DIR="Logs"
LOG_FILE_NAME="app.log"
os.makedirs(LOG_DIR, exist_ok=True)
log_path= os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)
voices= engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

#Level 1: The Mouth & Ears (Basic Input/Output)
#Speak Function: Create a function speak(text) that takes text and reads it out loud using pyttsx3.

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen Function: Create a function take_command() that uses the microphone to listen to the
# user and converts the audio into a string (text).


def take_command():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...............")
        r.pause_threshold=1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query= r.recognize_google(audio,language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        logging.info(e)
        print("Please say again...!")
        return "None"
    return query

# Greeting: When the program starts, Jarvis must greet the user based on the time of day (e.g., "Good
# Morning, Sir" if it's before 12 PM).

def greeting():
    hour = datetime.now().hour
    if(0<=hour<12):
        greeting="Good Morning Sir! How are you doing today!"
    elif(12<=hour<18):
        greeting="Good Afternoon Sir! How are you doing today!"
    else:
        greeting="Good Evening Sir! How are you doing today!"
    print(greeting)
    speak(greeting)

if __name__== "__main__":
 greeting()   
 speak("Hello! I am Jervis. I can Speak what ever is written")
 query=take_command().lower()
 print(query)

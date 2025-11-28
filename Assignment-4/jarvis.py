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
import re

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

# Level 2: The Worker (Automation Tasks)
# Tell Time: Command: "What time is it?" -> Jarvis replies with the current time.
# Wikipedia Search: Command: "Wikipedia [topic]" -> Jarvis reads the first 2 sentences of the summary
#from Wikipedia.
#Web Browser Automation:
# o "Open YouTube" -> Opens YouTube in the default browser.
# o "Open Google" -> Opens Google.
# o "Open LinkedIn" -> Opens the student's LinkedIn profile.

def get_current_time():
    now=datetime.now()
    str_time= now.strftime("%I:%M %p")
    return str_time

if __name__== "__main__":
 greeting()   
 speak("I am Jervis. I can Speak what ever is written")
 while True:
    query=take_command().lower()
    if not query: continue
    print(query)
    #pattern = r"\b(exit|bye|quit)\b"
    match(query):
        case _ if "time" in query:
            current_time=get_current_time()
            print(f"Sir the current time is {current_time}")
            speak(f"Sir the current time is {current_time}")
            logging.info("User asked for the current time.")
        case _ if any( x in query for x in ['bye','exit','quit']):
            #query.startswith(("exit", "bye", "quit")):
            #re.search(pattern, query):
            speak("Thank you Sir. Have a nice day.")
            logging.info("User exited the Program")
            exit()
        case _ if "wikipedia" in query:
            speak("Searching WIKI.....")
            query= query.replace("wikipedia","").strip()
            if not query:
                speak("What would you like me to search for on Wikipedia?")
                query = take_command().lower()
                if not query or "none" in query: 
                    speak("Okay, cancelling search.")
                    continue
            try:
                res= wikipedia.summary(query,sentences=2)
                speak("According to WIKI")
                speak(res)
                logging.info("User requested info from WIKI.")
            except wikipedia.exceptions.PageError:
                speak("I could not find any page matching that topic.")
                logging.warning(f"Wiki Page Not Found: {query}")    
            except Exception as e:
                speak('An error occurred while fetching the data.')
                logging.error(f"Wiki Error: {e}")
        case _ if "youtube" in query:
            speak("Opening YouTube")
            query = query.replace("youtube", "").strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            logging.info("User opened YouTube.")
        case _ if "google" in query:
            speak("Opening Google") 
            webbrowser.open("https://www.google.com")
            logging.info("User opened Google.") 
        case _ if "linkedin" in query:
            speak("Opening LinkedIn")
            webbrowser.open("https://www.linkedin.com/in/riasat-raihan")  # Replace with actual profile URL
            logging.info("User opened LinkedIn.")       

        case _:
            speak("I am sorry Sir, I am not trained to do this task yet.")



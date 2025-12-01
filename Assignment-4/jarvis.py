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
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Global variable to store Chrome driver instance
chrome_driver = None

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


# Function to open browser with Selenium
def open_browser_tab(url, site_name=None):
    global chrome_driver
    try:
        # Check if browser is still running if chrome_driver exists
        if chrome_driver is not None:
            try:
                # Try to access window handles to verify if browser is still running
                chrome_driver.window_handles
            except:
                # Browser was closed manually, reset the driver
                chrome_driver = None
        
        if chrome_driver is None:
            chrome_driver = webdriver.Chrome()
            chrome_driver.get(url)
        else:
            # Open URL in a new tab if browser is already open
            chrome_driver.execute_script(f"window.open('{url}', '_blank');")
            time.sleep(1)
            # Switch to the new tab
            chrome_driver.switch_to.window(chrome_driver.window_handles[-1])
        time.sleep(2)
        if site_name:
            speak(f"{site_name} opened successfully")
    except Exception as e:
        # Reset driver if any error occurs
        chrome_driver = None
        logging.error(f"Error opening browser: {e}")
        speak("Error opening browser")

# Function to close specific tab based on site name
def close_specific_tab(site_name):
    global chrome_driver
    try:
        if chrome_driver is None:
            speak("No browser is open")
            return False
        
        # Get all tabs and close the one matching the site
        for handle in chrome_driver.window_handles:
            chrome_driver.switch_to.window(handle)
            current_url = chrome_driver.current_url.lower()
            
            if site_name.lower() in current_url:
                chrome_driver.close()
                logging.info(f"Closed {site_name} tab")
                
                # If no more tabs, close the driver
                if len(chrome_driver.window_handles) == 0:
                    chrome_driver = None
                return True
        
        speak(f"Could not find {site_name} tab")
        logging.warning(f"Could not find {site_name} tab")
        return False
    except Exception as e:
        logging.error(f"Error closing tab: {e}")
        speak(f"Error closing {site_name} tab")
        return False

# Function to close entire browser
def close_browser():
    global chrome_driver
    try:
        if chrome_driver is not None:
            chrome_driver.quit()
            chrome_driver = None
            logging.info("Browser closed")
            return True
        return False
    except Exception as e:
        logging.error(f"Error closing browser: {e}")
        return False

# Level 3: The "Generative AI" Brain (Bootcamp Special)
#  Integration: Use the google-generativeai library (Gemini API) or openai library.
#  The "Think" Command: If the user asks a question that isn't a basic command (e.g., "Write a poem
# about Python" or "Explain Data Science"), Jarvis should send that text to the LLM and read out the
# answer.
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logging.warning("GEMINI_API_KEY environment variable not set")
    speak("API key not configured. Please set the GEMINI_API_KEY environment variable.")
else:
    genai.configure(api_key=API_KEY)

def ask_gemini(prompt):
    try:
        # Configuration for the specific model
        model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
        
        print(f"User: {prompt}")
        print("Gemini is thinking...")

        # Add instruction for short and concise answers
        modified_prompt = f"Answer in 2-3 sentences, concise and to the point: {prompt}"
        
        # Generate response
        response = model.generate_content(modified_prompt)
        
        # Extract and return text
        return response.text

    except Exception as e:
        return f"Error connecting to Gemini: {e}"


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
        case _ if "open youtube" in query:
            speak("Opening YouTube")
            query = query.replace("youtube", "").strip()
            url = f"https://www.youtube.com/results?search_query={query}"
            open_browser_tab(url, "YouTube")
            logging.info("User opened YouTube.")
        case _ if "open google" in query:
            speak("Opening Google")
            open_browser_tab("https://www.google.com", "Google")
            logging.info("User opened Google.") 
        case _ if "open linkedin" in query:
            speak("Opening LinkedIn")
            open_browser_tab("https://www.linkedin.com/in/riasat-raihan", "LinkedIn")
            logging.info("User opened LinkedIn.")
        case _ if "close youtube" in query or "close you tube" in query:
            speak("Closing YouTube tab")
            close_specific_tab("youtube")
            logging.info("User closed YouTube tab.")
        case _ if "close linkedin" in query:
            speak("Closing LinkedIn tab")
            close_specific_tab("linkedin")
            logging.info("User closed LinkedIn tab.")
        case _ if "close google" in query or "close chrome" in query or "close browser" in query:
            speak("Closing Chrome browser")
            close_browser()
            logging.info("User closed Chrome browser.")
        case _ if any( x in query for x in ['bye','exit','quit']):
            #query.startswith(("exit", "bye", "quit")):
            #re.search(pattern, query):
            speak("Thank you Sir. Have a nice day.")
            logging.info("User exited the Program")
            exit()  
        case _:
            response = ask_gemini(query)
            speak(response)
            logging.info("User asked for others question")



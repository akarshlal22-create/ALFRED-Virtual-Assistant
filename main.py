import os
import sys
import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from random import choice
from utils import opening_text
from pprint import pprint


# Read configured user name (defaults to User)
USERNAME = config('USER_NAME', default=config('USER', default='User'))
if not USERNAME or USERNAME == os.environ.get('USER'):
    USERNAME = 'User'
BOTNAME = config('BOTNAME', default='Alfred')


if sys.platform == 'win32':
    engine = pyttsx3.init('sapi5')
elif sys.platform == 'darwin':
    engine = pyttsx3.init('nsss')
else:
    engine = pyttsx3.init()

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    print(f"[{BOTNAME}]: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")


# Greet the user
def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak("Good Morning")
    elif (hour >= 12) and (hour < 16):
        speak("Good afternoon")
    elif (hour >= 16) and (hour < 19):
        speak("Good Evening")
    speak(f"I am {BOTNAME}. How may I assist you today?")


# Takes Input from User
def take_user_input(force_text=False):
    """Takes user input, recognizes it using Speech Recognition module or text input fallback"""
    query = 'None'

    if not force_text:
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print('\nListening....')
                r.pause_threshold = 1
                audio = r.listen(source, timeout=5, phrase_time_limit=8)

            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"[User (voice)]: {query}")
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            speak('Sorry, I could not understand. Could you please say that again?')
            return 'None'
        except Exception as e:
            print(f"\n[Microphone unavailable ({e}). Falling back to text input]")
            force_text = True

    if force_text or query == 'None':
        try:
            query = input(f"\n[{USERNAME}]: ").strip()
        except (KeyboardInterrupt, EOFError):
            query = 'exit'

    if not query:
        return 'None'

    if 'exit' in query.lower() or 'stop' in query.lower():
        hour = datetime.now().hour
        if hour >= 21 or hour < 6:
            speak("Good night, take care!")
        else:
            speak('Have a good day!')
        exit()
    else:
        speak(choice(opening_text))

    return query


if __name__ == '__main__':
    print("=" * 45)
    print(f"       {BOTNAME} Virtual Assistant")
    print("=" * 45)
    greet_user()

    force_text = '--text' in sys.argv or '-t' in sys.argv
    if not force_text and sys.stdin.isatty():
        choice_input = input("Input mode: [1] Voice (default) | [2] Text: ").strip()
        if choice_input == '2':
            force_text = True

    while True:
        query = take_user_input(force_text=force_text).lower()

        if 'who are you' in query or 'your name' in query:
            speak(f"I am {BOTNAME}, your virtual personal assistant, at your service.")

        elif 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do you want to search on Google?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak(
                'On what number should I send the message? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message.")

        elif "send an email" in query:
            speak("On what email address do I send? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject?")
            subject = take_user_input().capitalize()
            speak("What is the message?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs.")

        elif 'joke' in query:
            speak(f"Hope you like this one!")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Here's some advice for you:")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen.")
            pprint(advice)

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines:")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

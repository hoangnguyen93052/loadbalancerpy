import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random


class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.text_to_speech_engine = pyttsx3.init()
        self.commands = {
            "time": self.get_time,
            "date": self.get_date,
            "open browser": self.open_browser,
            "search": self.search_web,
            "joke": self.tell_joke,
            "weather": self.get_weather,
            "quit": self.quit_assistant,
        }
        self.jokes = [
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my computer I needed a break, and now it won’t stop sending me KitKat ads!",
            "Why don't scientists trust atoms? Because they make up everything!",
            "How does a penguin build its house? Igloos it together!",
        ]

    def speak(self, text):
        self.text_to_speech_engine.say(text)
        self.text_to_speech_engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return ""

    def get_time(self):
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {time_now}")

    def get_date(self):
        date_now = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today's date is {date_now}")

    def open_browser(self):
        webbrowser.open('http://www.google.com')
        self.speak("Opening the browser.")

    def search_web(self):
        self.speak("What do you want to search for?")
        query = self.listen()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.speak(f"Searching for {query} on the web.")

    def tell_joke(self):
        joke = random.choice(self.jokes)
        self.speak(joke)

    def get_weather(self):
        self.speak("I'm sorry, I can't check the weather right now.")

    def quit_assistant(self):
        self.speak("Goodbye!")
        exit()

    def execute_command(self, command):
        for key in self.commands:
            if key in command:
                self.commands[key]()
                return
        self.speak("I am sorry, I cannot perform that action.")

    def run(self):
        self.speak("Hello! I am your voice assistant. How can I help you today?")
        while True:
            command = self.listen()
            if command:
                self.execute_command(command)


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
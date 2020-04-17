import logging
import re

import pyttsx3 as pyttsx
import speech_recognition as sr
from nltk.chat import Chat

import settings
from chatbot.helpers import get_pairs, get_reflections


class Bot:
    heard = None
    responded = None
    pairs = None
    reflections = None
    chat = None

    listener = None
    speaker = None

    deaf = False
    dumb = False

    log_level = False

    def __init__(self, **kwargs):
        self.deaf = kwargs.get("deaf", False)
        self.dumb = kwargs.get("dumb", False)
        self.log_level = kwargs.get("log_level", False)

        self.log("Initializing")

        self.listener = sr.Recognizer()
        engine = pyttsx.init()
        self.speaker = engine

        self.pairs = get_pairs()
        self.reflections = get_reflections()

        print(self.pairs)
        print(self.reflections)

        self.chat = Chat(self.pairs, self.reflections)

        self.log("Initialized Bot.")

    def log(self, message):
        if self.log_level:
            log_level = self.log_level.lower()

            if log_level == 'debug':
                logging.debug(message)
            if log_level == 'info':
                logging.info(message)
            if log_level == 'warning':
                logging.warning(message)
            if log_level == 'error':
                logging.error(message)
            if log_level == 'critical':
                logging.critical(message)
            if log_level == 'console':
                print(message)

    def speak(self, message):
        if not self.dumb:
            self.speaker.say(message)
            self.speaker.runAndWait()
        else:
            print(message)

    def recognize(self, audio_source):
        recognized = self.listener.recognize_wit(audio_source, settings.WIT_AI_KEY)

        self.responded = self.respond(recognized)

        if not self.responded:
            self.responded = "I have no idea."

        return self.responded

    def respond(self, chat_query):
        # chat_query = message.lower()
        chat_response = self.chat.respond(chat_query)

        return chat_response

    def listen(self, prompt_text):
        if not self.deaf:
            self.speak(prompt_text)

            with sr.Microphone() as source:

                audio = self.listener.listen(source)

                try:
                    self.heard = self.recognize(audio)
                except sr.UnknownValueError:
                    self.heard = "I could not understand what you said."

                except sr.RequestError as e:
                    self.heard = "Error; %s" % e
        else:
            self.heard = input(prompt_text)


def main():
    homebot = Bot(deaf=False, dumb=False, log_level="console")

    homebot.speak("Welcome to home bot. Your robotic voice companion.")

    while True:
        homebot.listen("Please command me ")

        homebot.speak("I heard: %s" % homebot.heard)

        if re.match(r"quit|bye|goodbye|good\sbye|so\slong|farewell", homebot.heard.rstrip(".!")):
            break


if __name__ == "__main__":
    main()

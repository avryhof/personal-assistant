import re

import pyttsx3 as pyttsx
import speech_recognition as sr


class Bot:
    heard = None

    listener = None
    speaker = None

    deaf = False
    dumb = False

    def __init__(self, **kwargs):
        self.deaf = kwargs.get("deaf", False)
        self.dumb = kwargs.get("dumb", False)

        self.listener = sr.Recognizer()
        engine = pyttsx.init()
        self.speaker = engine

    def speak(self, message):
        if not self.dumb:
            self.speaker.say(message)
            self.speaker.runAndWait()
        else:
            print(message)

    def recognize(self, audio_source):

        return self.listener.recognize_sphinx(audio_source)

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
    homebot = Bot(deaf=True, dumb=False)

    while True:
        homebot.listen("> ")

        homebot.speak("I heard: %s" % homebot.heard)

        if re.match(r"quit|bye|goodbye|good\sbye|so\slong|farewell", homebot.heard.rstrip(".!")):  # statement == "quit":
            break


if __name__ == "__main__":
    main()

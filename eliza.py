import random
import re

import pyttsx
import speech_recognition as sr

"""
sphinx; CMU Sphinx(works offline)
google; Google Speech Recognition
google_cloud; Google Cloud Speech API
wit; Wit.ai
bing; Microsoft Bing Voice Recognition
houndify; Houndify API
ibm; IBM Speech to Text
"""
SPEECH_RECOGNITION = False

RECOGNITION_ENGINE = 'sphinx'
WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"  # Wit.ai keys are 32-character uppercase alphanumeric strings

r = sr.Recognizer()
eliza = engine = pyttsx.init()


def eliza_speak(message):
    print(message)

    if SPEECH_RECOGNITION:
        eliza.say(message)
        eliza.runAndWait()


def speech_recognize(audio_source):
    if RECOGNITION_ENGINE == 'sphinx':
        return r.recognize_sphinx(audio_source)

    if RECOGNITION_ENGINE == 'wit':
        return r.recognize_wit(audio_source, key=WIT_AI_KEY)


def audio_input(prompt_text):
    with sr.Microphone() as source:
        eliza_speak(prompt_text)
    audio = r.listen(source)

    try:
        return speech_recognize(audio)

    except sr.UnknownValueError:
        return "I could not understand what you said."

    except sr.RequestError as e:
        return "Error; {0}".format(e)


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])


def main():
    eliza_speak("Hello. How are you feeling today?")

    while True:
        if SPEECH_RECOGNITION:
            statement = audio_input("> ")

        else:
            statement = raw_input("> ")

        eliza_speak(analyze(statement))

        if re.match(r'quit|bye|goodbye|good\sbye|so\slong|farewell', statement.rstrip(".!")):  # statement == "quit":
            break


if __name__ == "__main__":
    main()

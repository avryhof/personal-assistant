import speech_recognition

import settings
from constants import RECOGNIZER_WIT, RECOGNIZER_SPHINX

sr = speech_recognition.Recognizer()


class SpeechRecognizer:
    sr = None
    engine = None

    def __init__(self, **kwargs):
        self.sr = sr
        self.engine = kwargs.get('engine', settings.RECOGNITION_ENGINE)

    def recognize(self, phrase):
        if self.engine == RECOGNIZER_SPHINX:
            retn = sr.recognize_sphinx(phrase)

        if self.engine == RECOGNIZER_WIT:
            retn = sr.recognize_wit(phrase, key=settings.WIT_AI_KEY)

    # def recognize_intents(self, phrase):
    #     """
    #     Ties the phrase to an utterance, and utterance to an intent.
    #     :param phrase:
    #     :return:
    #     """

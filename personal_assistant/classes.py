import glob
import inspect
import logging
import os
import re
import time
from importlib import import_module

import pyttsx3 as pyttsx
import speech_recognition as sr
import vlc
from rapidfuzz import fuzz, process

import settings


# class AssistantMediaClass(object):
#     player = None
#
#     def __init__(self, path=False):
#         if path:
#             self.load(path)
#
#     def load(self, path):
#         # self.player = vlc.MediaPlayer(path)
#         self.player = None
#
#     def pause(self):
#         self.player.pause()
#
#     def play(self):
#         self.player.play()
#
#     def stop(self):
#         self.player.stop()


class AssistantSkill(object):
    name = None
    utterances = []
    params = []
    param_values = dict()

    utterance_expressions = []

    def __init__(self, utterances=False):
        if self.name is None:
            self.name = re.sub("([A-Z])", " \\1", self.__class__.__name__).strip()

        if isinstance(utterances, str):
            self.utterances.append(utterances)

        if isinstance(utterances, list):
            for utterance in utterances:
                self.utterances.append(utterance)

        self.utterance_to_re()

    def utterance_to_re(self):
        re_parts = {"str": "[A-Za-z0-9 ]+?"}

        expression = r"<(.*?):(.*?)>"

        for utterance in self.utterances:
            new_utterance = utterance
            matches = re.findall(expression, utterance)
            for match in matches:
                replace_this = "<{}:{}>".format(match[0], match[1])
                with_this = "(?P<{}>{})".format(match[1], re_parts.get(match[0]))
                new_utterance = new_utterance.replace(replace_this, with_this)
                if new_utterance[-1] == ")":
                    new_utterance = "{}$".format(new_utterance)

            self.utterance_expressions.append(new_utterance)

    def get_param(self, param_name):
        return self.param_values.get(param_name, False)

    def parse(self, phrase):
        responded = False
        for utterance_expression in self.utterance_expressions:
            m = re.search(utterance_expression, phrase)
            if m is not None:
                responded = True
                for param in self.params:
                    try:
                        self.param_values.update({param: m.group(param)})
                    except IndexError:
                        pass
                if not self.handle():
                    responded = False

        return responded

    def handle(self):
        raise NotImplementedError("subclasses of AssistantSkill must provide a handle() method")

    def speak(self, phrase):
        phrase = self.param_values.get("phrase")
        bot = Bot(deaf=True, dumb=False, log_level=False)
        bot.speak(phrase)

    # @property
    # def media(self):
    #     return AssistantMediaClass()


class Bot:
    wake_word = "Speaker"

    gender = 0
    gender_values = dict(male=0, female=1)

    heard = None
    responded = None

    listener = None
    speaker = None

    microphone = False
    microphone_index = False

    deaf = False
    dumb = False

    log_level = False

    def __init__(self, **kwargs):
        self.deaf = kwargs.get("deaf", False)
        self.dumb = kwargs.get("dumb", False)
        self.log_level = kwargs.get("log_level", False)

        self.wake_word = kwargs.get("wake_word", "Eliza")

        gender_string = kwargs.get("gender", "male")
        self.gender = self.gender_values.get(gender_string.lower())

        self.log("Initializing")

        self.listener = sr.Recognizer()

        engine = pyttsx.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[self.gender].id)
        self.speaker = engine

        if not self.deaf and not self.microphone:
            self.configure_microphone()

        self._init_skills()

        self.log("Initialized Bot.")

    def _init_skills(self):
        skills_path_name = "skills"
        skills_module_name = "skills"
        skills_path = os.path.join(settings.BASE_DIR, skills_path_name)
        skills_directory = os.path.join(settings.BASE_DIR, skills_path)

        skills_directories = [
            directory for directory in glob.glob(os.path.join(skills_directory, "*")) if os.path.isdir(directory)
        ]

        for skill_path in skills_directories:
            skill_module_name = os.path.join(skill_path, "{}.py".format(skills_module_name))
            if os.path.exists(skill_module_name):
                skill_module_path = "{}.{}".format(
                    skill_path.replace(str(settings.BASE_DIR), "").replace(os.path.sep, "."), skills_module_name
                )[1::]
                skill_module = import_module(skill_module_path)

                for skill_class_name in dir(skill_module):
                    if skill_class_name != "AssistantSkill":
                        skill_class = getattr(skill_module, skill_class_name)

                        if inspect.isclass(skill_class) and issubclass(skill_class, AssistantSkill):
                            print("Found Skill: {}".format(skill_class.name))
                            settings.SKILLS_REGISTRY.append(skill_class)

    def log(self, message):
        if self.log_level:
            log_level = self.log_level.lower()

            if log_level == "debug":
                logging.debug(message)
            if log_level == "info":
                logging.info(message)
            if log_level == "warning":
                logging.warning(message)
            if log_level == "error":
                logging.error(message)
            if log_level == "critical":
                logging.critical(message)
            if log_level == "console":
                print(message)

    def detect_threshold(self):
        # self.speak("Determining ambient noise level. A moment of silence, please...")
        with self.microphone as source:
            self.listener.adjust_for_ambient_noise(source)
        time.sleep(1)

        self.log("Set minimum energy threshold to {}".format(self.listener.energy_threshold))

    def detect_microphone(self):
        # self.speak("Checking my ears.")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            # self.log('Microphone with name "{1}" found for `Microphone(device_index={0})`'.format(index, name))
            if "pulse" in name or "default" in name:
                self.microphone_index = index
                break

    def configure_microphone(self):
        self.detect_microphone()
        self.microphone = sr.Microphone(self.microphone_index)
        self.detect_threshold()

    def speak(self, message):
        if not self.dumb:
            self.speaker.say(message)
            self.speaker.runAndWait()
        else:
            print(message)

    def has_wake_word(self, phrase):
        phrase_parts = phrase.split()

        test_word = False
        start_index = 0
        retn = False

        if len(phrase_parts) == 1:
            test_word = phrase_parts[0]
            self.heard = ""

        elif len(phrase_parts) > 1:
            prefixes = ["ok", "hey"]

            test_word = False

            first_word, second_word = phrase_parts[0:2]
            extracted_processes = process.extract(first_word, prefixes)
            for extracted_process in extracted_processes:
                if extracted_process[1] > 80:
                    test_word = second_word
                    start_index = 2

            if not test_word:
                test_word = first_word
                start_index = 1

        if test_word and isinstance(test_word, str):
            fuzzed = fuzz.ratio(test_word.lower(), self.wake_word.lower())
            retn = fuzzed >= 80

        if retn:
            self.heard = " ".join(phrase_parts[start_index::])

        return retn

    def recognize(self, audio_source):
        recognized = self.listener.recognize_google(audio_source)
        # recognized = self.listener.recognize_sphinx(audio_source)

        self.log("You said: {}".format(recognized))

        return recognized

    def respond(self, chat_query):
        responded = False
        for skill in settings.SKILLS_REGISTRY:
            sc = skill()
            self.log("Trying {}".format(sc.name))
            try:
                responded = sc.parse(chat_query)
            except Exception as e:
                self.log(e)
            else:
                if responded:
                    break

        if not responded:
            self.log("I heard {} but could not respond.".format(chat_query))

        return responded

    def listen(self, prompt_text):
        if not self.deaf:
            self.speak(prompt_text)

            with self.microphone as source:
                self.log("Listening.")
                audio = self.listener.listen(source)
                self.log("Got it! Now to recognize it.")

                try:
                    self.heard = self.recognize(audio)
                except sr.UnknownValueError:
                    self.heard = "I could not understand what you said."

                except sr.RequestError as e:
                    self.heard = "Error; {}}".format(e)
        else:
            try:
                self.heard = input(prompt_text)
            except sr.UnknownValueError:
                self.heard = "I could not understand what you said."

            except sr.RequestError as e:
                self.heard = "Error; {}}".format(e)

        if self.has_wake_word(self.heard):
            self.responded = self.respond(self.heard)
        else:
            self.responded = False

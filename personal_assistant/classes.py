import datetime
import glob
import inspect
import logging
import os
import time
from importlib import import_module

import speech_recognition as sr
from rapidfuzz import fuzz, process

import settings
from skill_class import AssistantSkill


class Bot:
    wake_word = "Speaker"

    heard = None
    responded = None

    listener = None
    speaker = None

    microphone = False
    microphone_index = False

    deaf = False
    dumb = False
    gender_string = "male"

    log_level = False

    def __init__(self, **kwargs):
        self.deaf = kwargs.get("deaf", False)
        self.dumb = kwargs.get("dumb", False)
        load_skills = kwargs.get("load_skills", True)
        self.log_level = kwargs.get("log_level", False)

        self.wake_word = kwargs.get("wake_word", "Eliza")
        self.voice_language = kwargs.get("language", "english-us")

        self.log("Initializing")

        self.listener = sr.Recognizer()

        if not self.dumb:
            self.configure_tts()

        if not self.deaf and not self.microphone:
            self.configure_microphone()

        if load_skills:
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
                            if not hasattr(skill_class, "disabled") or not getattr(skill_class, "disabled"):
                                settings.SKILLS_REGISTRY.append(skill_class)
                            else:
                                self.log("{} skill is disabled.".format(skill_class.name))

    def log(self, message):
        if self.log_level:
            log_level = str(self.log_level).lower()

            debug_timestamp = datetime.datetime.now().isoformat()[0:19]
            debug_filename = os.path.basename(inspect.stack()[1][1])
            debug_function_name = inspect.stack()[1][3]
            debug_line_number = inspect.stack()[1][2]

            message = "%s - %s (%s):\n%s" % (debug_filename, debug_function_name, debug_line_number, message)

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

    def configure_tts(self):
        self.speaker = settings.tts

    def speak(self, message):
        if not self.dumb:
            self.speaker.synth(message)
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

import re

import vlc

import settings
from personal_assistant.base_class import BaseClass
from settings import tts
from utilities.debugging import log_message
from utilities.utility_functions import is_empty


class AssistantMediaClass(BaseClass):
    player = None

    def __init__(self, path=False, **kwargs):
        super().__init__(**kwargs)

        if path:
            self.load(path)

    def retn_code(self, retn_val):
        return True if retn_val >= 0 else False

    def load(self, path):
        try:
            self.player = vlc.MediaPlayer(path)
        except Exception as e:
            log_message(e)
        else:
            log_message("Loaded {}".format(path))

    def pause(self):
        return self.retn_code(self.player.pause())

    def play(self):
        return self.retn_code(self.player.play())

    def stop(self):
        return self.retn_code(self.player.stop())


class AssistantSkill(BaseClass):
    name = None
    utterances = []
    params = []
    param_values = dict()

    utterance_expressions = []

    def __init__(self, utterances=False, **kwargs):
        super().__init__(**kwargs)

        if self.name is None:
            self.name = re.sub("([A-Z])", " \\1", self.__class__.__name__).strip()

        if isinstance(utterances, str):
            self.utterances.append(utterances)

        self.utterance_expressions = []
        if isinstance(utterances, list):
            for utterance in utterances:
                self.utterances.append(utterance)

        self.utterance_to_re()
        self.media = AssistantMediaClass()

    def __str__(self):
        if not is_empty(self.name):
            return self.name
        else:
            return self.__class__.name

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
        should_respond = False
        responded = False
        match_phrase = phrase.strip().lower()

        self.log(self.name, self.utterance_expressions)

        for utterance_expression in self.utterance_expressions:
            if match_phrase == utterance_expression or re.search(
                utterance_expression, match_phrase
            ):

                m = re.search(utterance_expression, match_phrase)
                if m is not None:
                    for param in self.params:
                        try:
                            self.param_values.update({param: m.group(param)})
                        except IndexError:
                            pass

                responded = self.handle()
                if responded:
                    break

        return responded

    def handle(self):
        raise NotImplementedError(
            "subclasses of AssistantSkill must provide a handle() method"
        )

    def speak(self, phrase=None):
        if phrase is None:
            phrase = self.param_values.get("phrase")

        if settings.DUMB:
            print(phrase)
        else:
            tts.synth(phrase)

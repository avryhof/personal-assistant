import re

from settings import tts


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
                self.handle()

        return responded

    def handle(self):
        raise NotImplementedError("subclasses of BaseCommand must provide a handle() method")

    def speak(self, phrase):
        phrase = self.param_values.get("phrase")
        tts.synth(phrase)

import random

from bot_class import Bot
from skill_class import AssistantSkill


class SpeakSkill(AssistantSkill):
    utterances = ["say <str:phrase>", "repeat <str:phrase>"]
    params = ["phrase"]

    def handle(self):
        phrase = self.param_values.get("phrase")
        self.speak(phrase)


class ExitSkill(AssistantSkill):
    utterances = ["exit", "goodbye", "quit", "so long", "farewell"]

    def handle(self):
        self.speak(random.choice(["goodbye", "have a nice day"]))
        exit()


class HelloSkill(AssistantSkill):
    utterances = ["hi", "hello", "howdy"]

    def handle(self):
        phrase = random.choice(self.utterances)
        print("Saying: {}".format(phrase))
        self.speak(phrase)
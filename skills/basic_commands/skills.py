import random

from personal_assistant.assistant_skill_class import AssistantSkill


class SpeakSkill(AssistantSkill):
    name = "Speak Skill"
    utterances = ["say <str:phrase>", "repeat <str:phrase>"]
    params = ["phrase"]

    def handle(self):
        phrase = self.param_values.get("phrase")
        self.speak(phrase)

        return True


class ExitSkill(AssistantSkill):
    name = "Exit Skill"
    utterances = ["exit", "goodbye", "quit", "so long", "farewell"]

    def handle(self):
        self.speak(random.choice(["goodbye", "have a nice day", "so long", "sionara", "have a good one"]))
        exit()


class HelloSkill(AssistantSkill):
    name = "Hello Skill"
    utterances = ["hi", "hello", "howdy", "hola", "hidey-ho"]

    def handle(self):
        phrase = random.choice(self.utterances)
        self.log("Saying: {}".format(phrase))
        self.speak(phrase)

        return True

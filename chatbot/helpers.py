from nltk.chat.util import reflections

from chatbot.models import NLTKReflections, NLTKPairs


def get_reflections():
    return_reflections = reflections

    for my_reflection in NLTKReflections.filter(active=True):
        return_reflections.update({my_reflection.reflection_phrase: my_reflection.reflection})

    return return_reflections


def get_pairs():
    pairs = []

    nltk_pairs = NLTKPairs.filter(active=True)

    for pair in nltk_pairs:
        pairs.append([pair.question, [pair.answer]])

    return pairs


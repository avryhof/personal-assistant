import pprint
import re

utterances = ["say <str:phrase> to me", "play <str:song> by <str:artist>"]
params = ["phrase", "song", "artist"]
utterance_expressions = []

re_parts = {"str": "[A-Za-z0-9 ]+?"}

expression = r"<(.*?):(.*?)>"

for utterance in utterances:
    new_utterance = utterance
    matches = re.findall(expression, utterance)
    for match in matches:
        replace_this = "<{}:{}>".format(match[0], match[1])
        with_this = "(?P<{}>{})".format(match[1], re_parts.get(match[0]))
        new_utterance = new_utterance.replace(replace_this, with_this)
        if new_utterance[-1] == ")":
            new_utterance = "{}$".format(new_utterance)
    # print(utterance)
    # print(new_utterance)
    utterance_expressions.append(new_utterance)

phrase = "play the sound of silence by simon and garfunkel"

for utterance_expression in utterance_expressions:
    m = re.search(utterance_expression, phrase)
    if m is not None:
        # print(m.groups())
        kwargs = {}
        for param in params:
            try:
                kwargs.update({param: m.group(param)})
                # print(m.group(param))
            except IndexError:
                pass
        pprint.pprint(kwargs)

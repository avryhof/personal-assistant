import nltk

sentence = "Turn on the lights in the livingroom."

tokens = nltk.word_tokenize(sentence)
print(tokens)

tagged = nltk.pos_tag(tokens)
print(tagged[0:6])

entities = nltk.chunk.ne_chunk(tagged)
print(entities)
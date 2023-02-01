import nltk

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

sentence = "Turn on the lights in the livingroom."

tokens = nltk.word_tokenize(sentence)
print(tokens)

tagged = nltk.pos_tag(tokens)
print(tagged[0:6])

entities = nltk.chunk.ne_chunk(tagged)
print(entities)
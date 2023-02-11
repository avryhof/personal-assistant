import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty("voices")

for voice in list(voices):
    print(voice)

# engine.say("I will speak this text")
# engine.runAndWait()

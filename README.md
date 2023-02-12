# Personal Assistant

A simple and lightweight personal assistant.

Pretty simple -

* It listens for a wake word (just the word or "hey <wake word>" or "ok <wake word>")
* Loops through skill classes until it finds a matching utterance
* Uses the Skill class parser() method to parse what you asked the skill to do
* Uses the Skill class respond() method to generate a response
* If no skills responded, it can be passed to ChatGPT and the response will be generated from there
    * There is also an NLTK responder in the works. It supports the default NLTK reflections and responders, but still
      needs a bit more development.

## Technologies

* Captures audio with the speech_recognition module
    * Currently uses the Google speech recognizer - I really want this offline, but sphinx isn't quite there, and I'm
      not really sure if I want to get into something as heavy as Vosk just yet.
* Responds with pyttsx3, so it will adapt to whatever TTS layer is on your computer

## Notes

- Should add support for [Precise](https://github.com/MycroftAI/mycroft-precise)

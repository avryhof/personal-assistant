# Personal Assistant
A simple and lightweight personal assistant.

Built with [my fork](https://pypi.org/project/speech-recognition-fork/) of [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) and [pyttsx3](https://pypi.org/project/pyttsx3/)

So far it has:
- Custom Wake word
- Custom "Gender"
- Skill Classes loosely based on Django Views
- Classes for (still building skills)
    - Philips Hue
    - Subsonic
    
### Notes
- SpeechRecognition supports a few offline recognizers.
    - Sphinx: It sort of works, but the accuracy is pretty bad
    - Snowboy: Not open source
- Should add support for [Precise](https://github.com/MycroftAI/mycroft-precise)
- Skill parser is RexEx based, but utterances can be defined similar to path() statements in Django.


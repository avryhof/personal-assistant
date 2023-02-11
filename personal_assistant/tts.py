import pyttsx3 as pyttsx

from personal_assistant.base_class import BaseClass
from utilities.utility_functions import is_empty


class PyTTSX3(BaseClass):
    """A TTS-Wrapper compatible module for pyttsx3"""
    engine = pyttsx.init()

    def __init__(self, voice_name=None, rate=175) -> None:
        voices = self.engine.getProperty("voices")

        if not is_empty(voice_name):
            for voice in list(voices):
                if voice_name.upper() in voice.name.upper():
                    self.engine.setProperty("voice", voice.id)

        self.engine.setProperty("rate", rate)  # setting up new voice rate

    def _wrap_ssml(self, ssml) -> str:
        # Don't force-wrap SSML.
        return ssml

    def synth(self, ssml: str, filename=None) -> None:
        """SSML will actually be stripped"""
        if filename is not None:
            self.engine.save_to_file(ssml, filename)
        else:
            self.engine.say(ssml)
        self.engine.runAndWait()

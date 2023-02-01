import os
from pathlib import Path

from tts_wrapper import PicoClient, SAPIClient, SAPITTS

from personal_assistant.constants import RECOGNIZER_WIT

BASE_DIR = Path(__file__).resolve().parent

# client = PicoClient()
client = SAPIClient()
tts = SAPITTS(client)

DEBUG = False

DEAF = True
DUMB = True

# RECOGNITION_ENGINE = RECOGNIZER_SNOWBOY
# RECOGNITION_ENGINE = RECOGNIZER_SPHINX
RECOGNITION_ENGINE = RECOGNIZER_WIT

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# BASE_RESPONDER = "chatgpt"
BASE_RESPONDER = "nltk"

WIT_AI_KEY = os.environ.get("WIT_ACCESS_TOKEN")

SKILLS_REGISTRY = []

import os
from pathlib import Path

from personal_assistant.constants import RECOGNIZER_WIT
from personal_assistant.tts import PyTTSX3

BASE_DIR = Path(__file__).resolve().parent

tts = PyTTSX3(voice_name="zira")

DEBUG = False
LOG_LEVEL = "quiet console"

DEAF = True
DUMB = False

# RECOGNITION_ENGINE = RECOGNIZER_SNOWBOY
# RECOGNITION_ENGINE = RECOGNIZER_SPHINX
RECOGNITION_ENGINE = RECOGNIZER_WIT

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEOIP_KEY = os.environ.get("GEOIP_KEY")
NWS_EMAIL = "amos@vryhof.net"

BASE_RESPONDER = "chatgpt"
# BASE_RESPONDER = "nltk"

WIT_AI_KEY = os.environ.get("WIT_ACCESS_TOKEN")

SKILLS_REGISTRY = []

LOCATION = None

